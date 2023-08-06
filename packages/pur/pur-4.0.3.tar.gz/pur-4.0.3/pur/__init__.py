# -*- coding: utf-8 -*-
"""
    pur
    ~~~
    Update packages in a requirements.txt file to latest versions.
    :copyright: (c) 2016 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""


import click
import os
import re
import sys
try:
    from StringIO import StringIO
except ImportError:  # pragma: nocover
    from io import StringIO

# add local packages folder to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'packages'))
try:
    from pip._internal.download import PipSession
except (TypeError, ImportError):  # pragma: nocover
    # on Windows, non-ASCII characters in import path can be fixed using
    # the script path from sys.argv[0].
    # More info at https://github.com/wakatime/wakatime/issues/32
    sys.path.insert(0,
                    os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                                 'packages'))
    from pip._internal.download import PipSession


from pip._internal.download import get_file_content
from pip._internal.exceptions import InstallationError
from pip._internal.index import PackageFinder
from pip._internal.models.index import PyPI
from pip._internal.req import req_file
from pip._internal.req.req_install import Version
from pip._vendor.packaging.version import InvalidVersion

from .__about__ import __version__
from .exceptions import StopUpdating


@click.command()
@click.option('-r', '--requirement', type=click.Path(),
              help='The requirements.txt file to update; Defaults to using ' +
              'requirements.txt from the current directory if it exist.')
@click.option('-o', '--output', type=click.Path(),
              help='Output updated packages to this file; Defaults to ' +
              'overwriting the input requirements.txt file.')
@click.option('-i', '--interactive', is_flag=True, default=False,
              help='Interactively prompts before updating each package.')
@click.option('-f', '--force', is_flag=True, default=False,
              help='Force updating packages even when a package has no ' +
              'version specified in the input requirements.txt file.')
@click.option('-d', '--dry-run', is_flag=True, default=False,
              help='Output changes to STDOUT instead of overwriting the ' +
              'requirements.txt file.')
@click.option('-n', '--no-recursive', is_flag=True, default=False,
              help='Prevents updating nested requirements files.')
@click.option('-s', '--skip', type=click.STRING, help='Comma separated list ' +
              'of packages to skip updating.')
@click.option('--only', type=click.STRING, help='Comma separated list of ' +
              'packages. Only these packages will be updated.')
@click.option('-z', '--nonzero-exit-code', is_flag=True, default=False,
              help='Exit with status l0 when all packages up-to-date, 11 ' +
              'when some packages were updated. Defaults to exit status zero ' +
              'on success and non-zero on failure.')
@click.version_option(__version__)
def pur(**options):
    """Command line entry point."""

    if not options['requirement']:
        options['requirement'] = 'requirements.txt'
    try:
        options['skip'] = set(x.strip().lower() for x in options['skip'].split(','))
    except AttributeError:
        options['skip'] = set()
    try:
        options['only'] = set(x.strip().lower() for x in options['only'].split(','))
    except AttributeError:
        options['only'] = set()

    global UPDATED
    UPDATED = 0

    # patch pip for handling nested requirements files
    patch_pip(options)

    output_filename = options['output'] or options['requirement']
    update_requirements(options['requirement'], output_filename, options)

    echo('All requirements up-to-date.', **options)

    if options['nonzero_exit_code']:
        if UPDATED > 0:
            raise ExitCodeException(11)
        raise ExitCodeException(10)


UPDATED = 0


def update_requirements(filename, output_filename, options):
    """Update a requirements file.

    Returns the number of updated packages as an int.

    :param filename:        Path to a requirements.txt file.
    :param output_filename: Path to the output requirements.txt file.
    :param options:         Dict containing original command line arguments.
    """

    global UPDATED

    updated = 0
    buf = StringIO()

    try:
        requirements = get_requirements_and_latest(filename,
                                                   force=options['force'])

        stop = False
        for line, req, spec_ver, latest_ver in requirements:

            if (not stop and req and req.name.lower() not in options['skip'] and (len(options['only']) == 0 or req.name.lower() in options['only'])):

                try:
                    if should_update(req, spec_ver, latest_ver,
                                    force=options['force'],
                                    interactive=options['interactive']):

                        if not spec_ver[0]:
                            new_line = '{0}=={1}'.format(line, latest_ver)
                        else:
                            new_line = update_requirement(req, line, spec_ver,
                                                        latest_ver)
                        buf.write(new_line)

                        if new_line != line:
                            echo('Updated {package}: {old} -> {new}'.format(
                                package=req.name,
                                old=old_version(spec_ver),
                                new=latest_ver,
                            ), **options)
                            updated += 1
                        else:
                            msg = ('New version for {package} found ({new}), ' +
                                   'but current spec prohibits updating: ' +
                                   '{line}')
                            echo(msg.format(
                                package=req.name,
                                new=latest_ver,
                                line=line,
                            ), **options)

                    else:
                        buf.write(line)
                except StopUpdating:
                    stop = True
                    buf.write(line)

            else:
                buf.write(line)

            buf.write("\n")

    except InstallationError as e:
        raise click.ClickException(str(e))

    if not options['dry_run']:
        with open(output_filename, 'w') as output:
            output.write(buf.getvalue())
    else:
        echo('==> ' + output_filename + ' <==')
        echo(buf.getvalue())

    buf.close()

    UPDATED += updated


def patch_pip(options):
    """Patch pip to also update nested requirements files.

    :param options:  Dict containing original command line arguments.
    """

    global UPDATED
    seen = []

    def patched_parse_requirements(*args, **kwargs):
        global UPDATED
        if not options['no_recursive']:
            filename = args[0]
            if not options['output'] and filename not in seen:
                if os.path.isfile(filename):
                    seen.append(filename)
                    update_requirements(filename, filename, options)
        return []
    req_file.parse_requirements = patched_parse_requirements


def get_requirements_and_latest(filename, force=False):
    """Parse a requirements file and get latest version for each requirement.

    Yields a tuple of (original line, InstallRequirement instance,
    spec_versions, latest_version).

    :param filename:  Path to a requirements.txt file.
    :param force:     Force getting latest version even for packages without
                      a version specified.
    """
    session = PipSession()
    finder = PackageFinder(
        session=session, find_links=[], index_urls=[PyPI.simple_url])

    _, content = get_file_content(filename, session=session)
    for line_number, line, orig_line in yield_lines(content):
        line = req_file.COMMENT_RE.sub('', line)
        line = line.strip()
        req = parse_requirement_line(line, filename, line_number, session, finder)
        if req is None or req.name is None or req_file.SCHEME_RE.match(req.name):
            yield (orig_line, None, None, None)
            continue
        spec_ver = current_version(req)
        if spec_ver or force:
            latest_ver = latest_version(req, session, finder)
            yield (orig_line, req, spec_ver, latest_ver)


def parse_requirement_line(line, filename, line_number, session, finder):
    """Parse a requirement line and return an InstallRequirement instance.

    :param line:         One line from a requirements.txt file.
    :param filename:     Path to a requirements.txt file.
    :param line_number:  The integer line number of the current line.
    :param session:      Instance of pip.download.PipSession.
    :param finder:       Instance of pip.download.PackageFinder.
    """

    if not line:
        return None

    reqs = list(req_file.process_line(
                line, filename, line_number, session=session, finder=finder))
    return reqs[0] if len(reqs) > 0 else None


def current_version(req):
    """Get the current version from an InstallRequirement instance.

    Returns a tuple (found, eq_ver, gt_ver, gte_ver, lt_ver, lte_ver, not_ver).
    The versions in the returned tuple will be either a
    pip.req.req_install.Version instance or None.

    :param req:    Instance of pip.req.req_install.InstallRequirement.
    """

    eq_ver = None
    gt_ver = None
    gte_ver = None
    lt_ver = None
    lte_ver = None
    not_ver = None
    for spec in req.req.specifier:
        operator, version = spec._spec
        try:
            ver = Version(version)
        except InvalidVersion:
            continue
        if operator == '==':
            eq_ver = ver
        elif operator == '>':
            if not gt_ver or ver > gt_ver:
                gt_ver = ver
        elif operator == '>=':
            if not gte_ver or ver > gte_ver:
                gte_ver = ver
        elif operator == '<':
            if not lt_ver or ver < lt_ver:
                lt_ver = ver
        elif operator == '<=':
            if not lte_ver or ver < lte_ver:
                lte_ver = ver
        elif operator == '!=':
            not_ver = ver

    found = (eq_ver is not None or gt_ver is not None or gte_ver is not None or
             lt_ver is not None or lte_ver is not None or not_ver is not None)

    return found, eq_ver, gt_ver, gte_ver, lt_ver, lte_ver, not_ver


def old_version(spec_ver):
    """Get the old version that was updated.

    :param spec_ver:  A tuple from current_version.
    """

    eq_ver = spec_ver[1]
    gte_ver = spec_ver[3]

    if eq_ver is not None:
        return eq_ver

    if gte_ver is not None:
        return gte_ver

    return 'Unknown'


def yield_lines(content):
    """Yields a tuple of each line in a requirements file string.

    The tuple contains (lineno, joined_line, original_line).

    :param content:  Text content of a requirements.txt file.
    """
    lines = content.splitlines()
    for lineno, joined, orig in join_lines(enumerate(lines, start=1)):
        yield lineno, joined, orig


def join_lines(lines_enum):
    """Joins a line ending in '\' with the previous line.

    (except when following comments). The joined line takes on the index of the
    first line.
    """
    COMMENT_RE = re.compile(r'(^|\s)+#.*$')
    primary_line_number = None
    new_line = []
    orig_lines = []
    for line_number, orig_line in lines_enum:
        line = orig_line
        if not line.endswith('\\') or COMMENT_RE.match(line):
            if COMMENT_RE.match(line):
                # this ensures comments are always matched later
                line = ' ' + line
            if new_line:
                new_line.append(line)
                orig_lines.append(orig_line)
                yield (primary_line_number, ''.join(new_line),
                       "\n".join(orig_lines))
                new_line = []
                orig_lines = []
            else:
                yield line_number, line, orig_line
        else:
            if not new_line:
                primary_line_number = line_number
            new_line.append(line.rstrip('\\'))
            orig_lines.append(orig_line)

    # last line contains \
    if new_line:
        yield primary_line_number, ''.join(new_line), "\n".join(orig_lines)


def latest_version(req, session, finder, include_prereleases=False):
    """Returns a Version instance with the latest version for the package.

    :param req:                 Instance of
                                pip.req.req_install.InstallRequirement.
    :param session:             Instance of pip.download.PipSession.
    :param finder:              Instance of pip.download.PackageFinder.
    :param include_prereleases: Include prereleased beta versions.
    """
    if not req:  # pragma: nocover
        return None

    all_candidates = finder.find_all_candidates(req.name)

    if not include_prereleases:
        all_candidates = [candidate for candidate in all_candidates
                          if not candidate.version.is_prerelease]

    if not all_candidates:
        return None

    best_candidate = max(all_candidates,
                         key=finder._candidate_sort_key)
    remote_version = best_candidate.version
    return remote_version


def should_update(req, spec_ver, latest_ver, force=False, interactive=False):
    """Returns True if this requirement should be updated, False otherwise.

    :param req:         Instance of pip.req.req_install.InstallRequirement.
    :param spec_ver:    Tuple of current versions from the requirements file.
    :param latest_ver:  Latest version from pypi.
    :param force:       Force getting latest version even for packages without
                        a version specified.
    """

    if latest_ver is None:
        return False

    found = spec_ver[0]
    eq_ver = spec_ver[1]
    lt_ver = spec_ver[4]
    lte_ver = spec_ver[5]
    not_ver = spec_ver[6]

    if not found and (not force or req.link is not None):
        return False

    if eq_ver is not None and latest_ver <= eq_ver:
        return False

    if not_ver is not None and latest_ver == not_ver:
        return False

    if lt_ver is not None and not latest_ver < lt_ver:
        return False

    if lte_ver is not None and not latest_ver <= lte_ver:
        return False

    return not interactive or ask_to_update(req, spec_ver, latest_ver)


def ask_to_update(req, spec_ver, latest_ver):
    """Prompts to update the current package.

    Returns True if should update, False if should skip, and raises
    SaveAndStopUpdating or StopUpdating exceptions if the user selected quit.

    :param req:         Instance of pip.req.req_install.InstallRequirement.
    :param spec_ver:    Tuple of current versions from the requirements file.
    :param latest_ver:  Latest version from pypi.
    """

    choices = ['y', 'n', 'q']

    msg = 'Update {package} from {old} to {new}? ({choices})'.format(
        package=req.name,
        old=old_version(spec_ver),
        new=latest_ver,
        choices=', '.join(choices),
    )
    while True:
        value = click.prompt(msg, default='y')
        value = value.lower()
        if value in choices:
            break
        echo('Please enter either {0}.'.format(', '.join(choices)))

    if value == 'y':
        return True
    if value == 'n':
        return False

    # when value == 'q'
    raise StopUpdating()


def update_requirement(req, line, spec_ver, latest_ver):
    """Updates the version of a requirement line.

    Returns a new requirement line with the package version updated.

    :param req:         Instance of pip.req.req_install.InstallRequirement.
    :param line:        The requirement line string.
    :param spec_ver:    Tuple of current versions from the requirements file.
    :param latest_ver:  Latest version from pypi.
    """

    start_of_spec = (line.index(']') + 1 if ']' in line.split('#')[0]
                     else len(req.name))
    package_part = line[:start_of_spec]
    spec_part = line[start_of_spec:]

    old_ver = spec_ver[1] or spec_ver[3]
    spec_regex = re.sub(r'(\W)', r'\\\1', str(old_ver))
    pattern = r'((==|>=)\s*){0}'.format(spec_regex)
    match = re.search(pattern, spec_part)
    if match is None:
        return line
    pre_part = match.group(1)
    old = '{0}{1}'.format(pre_part, str(old_ver))
    new = '{0}{1}'.format(pre_part, str(latest_ver))
    new_line = '{package_part}{spec_part}'.format(
        package_part=package_part,
        spec_part=spec_part.replace(old, new, 1),
    )
    return new_line


def echo(msg, dry_run=False, **kwargs):
    if not dry_run:
        click.echo(msg)


class ExitCodeException(click.ClickException):
    def __init__(self, exit_code):
        self.exit_code = exit_code

    def show(self):
        pass

"""CLI interface for the package"""

import logging
import os
import re

import click

from . import logging as rpmlb_logging
from .builder.base import BaseBuilder
from .downloader.base import BaseDownloader
from .recipe import Recipe
from .work import Work

DIST_RE = re.compile('^(fc|el|centos)[0-9]*$')


@click.command(add_help_option=False)
# General options
@click.help_option('--help', '-h')  # Enable short help switch (-h)
@click.version_option()
@click.option(
    '--verbose', '-v', is_flag=True, default=False,
    help='Turn on verbose logging.',
    # Enable logging as early as possible
    is_eager=True, expose_value=False,
    callback=lambda ctx, param, verbose:
        rpmlb_logging.configure_logging(verbose),
)
@click.option(
    '--download', '-d',
    type=click.Choice('none local fedpkg rhpkg custom'.split()),
    default='none',
    help='Choose a download type.',
)
@click.option(
    '--build', '-b',
    type=click.Choice('dummy mock copr koji custom'.split()),
    default='dummy',
    help='Choose a build type.',
)
@click.option(
    '--work-directory', '-w', metavar='WORK_DIRECTORY',
    type=click.Path(exists=True, file_okay=False, writable=True,
                    resolve_path=True),
    default=None,
    help='Specify a working directory.',
)
@click.option(
    '--custom-file', '-c', metavar='CUSTOM_FILE',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help='Instructions for custom downloader and builder.',
)
@click.option(
    '--dist', metavar=DIST_RE.pattern,
    help='Specifiy a distribution platform considered in a recipe file.',
    callback=lambda ctx, param, dist: validate_dist(dist),
)
# Download options
@click.option(
    '--branch', '-B', metavar='BRANCH',
    help=('Git branch for downloaders that use it '
          '(download type: fedpkg, rhpkg).'),
)
@click.option(
    '--source-directory', '-S', metavar='SOURCE_DIRECTORY',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    default=os.path.abspath(os.getcwd()),
    help='Package source directory for local downloader.',
)
# Build options
@click.option(
    '--resume', '-r', metavar='RESUME',
    type=click.INT,
    help='Resume build from specified position.',
)
@click.option(
    '--retry', metavar='RETRY_COUNT',
    type=click.IntRange(min=0), default=0,  # no negatives
    help='Retry failed build RETRY_COUNT times before aborting.',
)
@click.option(
    '--pkg-cmd',
    type=click.Choice('fedpkg rhpkg'.split()),
    help='Choose a package command.',
)
@click.option(
    '--mock-config', '-M', metavar='MOCK_CONFIG',
    help='Mock configuration for mock builder.',
)
@click.option(
    '--copr-repo', '-C', metavar='COPR_REPO',
    help='Target Copr for copr builder.',
)
@click.option(
    '--koji-epel', metavar='VERSION', type=int, default=7,
    help='Target EPEL version for koji builder.',
)
@click.option(
    '--koji-profile', metavar='PROFILE',
    help='Configuration profile for koji builder.',
)
@click.option(
    '--koji-target-format', metavar='FORMAT',
    help='Target format string for koji builder.',
)
@click.option(
    '--koji-scratch', is_flag=True, default=False,
    help='Make scratch builds with koji builder.',
)
@click.option(
    '--koji-owner', metavar='OWNER',
    help='Owner of packages added by koji builder.',
)
# Positional arguments
@click.argument(
    'recipe_file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.argument('collection_id')
def run(recipe_file, collection_id, **option_dict):
    """Download and build RPMs listed in RECIPE_FILE under COLLECTION_ID
    (such as 'python33').
    """

    log = logging.getLogger(__name__)

    _choose_pkg_cmd(option_dict)

    # Load recipe and processing objects
    recipe = Recipe(recipe_file, collection_id)
    recipe.verify()

    # Prepare the working directory
    # HINT: with contextlib.closing(Work(recipe, **option_dict)) as work:
    work = Work(recipe, **option_dict)

    builder = BaseBuilder.get_instance(
        option_dict['build'],
        work,
        **option_dict
    )
    downloader = BaseDownloader.get_instance(option_dict['download'])

    # Download
    log.info('Downloading...')
    downloader.run(work, **option_dict)

    # Build
    log.info('Building...')
    builder.run(work, **option_dict)

    log.info('Success!')


def validate_dist(dist):
    if dist and not DIST_RE.match(dist):
        raise click.BadParameter(
            'dist shoule be match to pattern {0}'.format(DIST_RE.pattern))
    return dist


def _choose_pkg_cmd(option_dict):
    if not option_dict:
        return
    # User chose the command explicitly.
    if 'pkg_cmd' in option_dict and option_dict['pkg_cmd']:
        return

    # Set default value.
    option_dict['pkg_cmd'] = 'fedpkg'

    download = option_dict.get('download', None)
    # No explicit command, but relevant builder was selected.
    if download in ('fedpkg', 'rhpkg'):
        option_dict['pkg_cmd'] = download

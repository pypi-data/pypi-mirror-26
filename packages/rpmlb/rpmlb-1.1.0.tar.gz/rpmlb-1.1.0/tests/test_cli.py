"""Test argument parsing"""

import logging
import os
from contextlib import ExitStack
from pathlib import Path
from textwrap import dedent

import click
import pytest
from click.testing import CliRunner

from rpmlb import cli


@pytest.fixture
def root_logger():
    return logging.getLogger()


@pytest.fixture
def runner(root_logger):
    r = CliRunner()

    with r.isolated_filesystem():
        yield r


@pytest.fixture
def recipe_path(tmpdir):
    """Test recipe file path"""

    with tmpdir.as_cwd():
        path = Path.cwd().resolve() / 'recipe.yml'

        # Fill in valid but empty recipe content
        with path.open(mode='w', encoding='utf-8') as outfile:
            contents = dedent('''\
                test:
                    name: Test recipe
                    requires: []
                    packages:
                        - test
                ''')
            print(contents, file=outfile)

        yield path


@pytest.fixture
def recipe_arguments(recipe_path):
    """Common recipe arguments: Path to the recipe file and recipe name."""

    return [str(recipe_path), 'test']


@pytest.mark.parametrize('option', ('recipe_file', 'collection_id', 'build',
                                    'download', 'branch', 'source_directory',
                                    'pkg_cmd'))
def test_parse_argv_no_options(tmpdir, option):
    """Tests proper default values of the CLI"""

    recipe_file = tmpdir.join('ror.yml')
    collection_id = 'rh-ror50'

    # Prepare environment
    recipe_file.write('')

    current_dir = os.path.abspath(os.getcwd())

    expected = {
        'recipe_file': str(recipe_file),
        'collection_id': str(collection_id),
        'build': 'dummy',
        'download': 'none',
        'branch': None,
        'source_directory': current_dir,
        'pkg_cmd': None,
    }

    # Parse the arguments
    with tmpdir.as_cwd():
        argv = list(map(str, [recipe_file, collection_id]))
        args = cli.run.make_context('rpmlb', argv).params

        assert args[option] == expected[option]


@pytest.mark.parametrize('verbose', (True, False))
def test_log_verbosity(root_logger, runner, verbose, recipe_arguments):
    """Ensure that the verbosity is set properly on."""

    verbose_args = ['--verbose'] if verbose else []
    level = logging.DEBUG if verbose else logging.INFO

    runner.invoke(cli.run, verbose_args + recipe_arguments)
    assert root_logger.getEffectiveLevel() == level


@pytest.fixture(params=('work-directory', 'custom-file'))
def path_kind(request):
    return request.param


def path_options(path_kind):
    """Excepted environment for the path tests"""
    filename = 'custom.yml' if path_kind == 'custom-file' else path_kind

    root = Path.cwd().resolve()
    path = root/filename

    options = ['--' + path_kind, str(path)]

    assert not path.exists()

    return path, options


def test_path_nonexistent(runner, path_kind, recipe_arguments):
    path, options = path_options(path_kind)

    result = runner.invoke(cli.run, options + recipe_arguments,
                           standalone_mode=False)
    assert result.exception is not None
    assert isinstance(result.exception, click.BadParameter)


def test_path_expected_and_absolute(path_kind, recipe_arguments):
    path, options = path_options(path_kind)

    if path_kind.endswith('directory'):
        path.mkdir()
    else:
        path.touch(mode=0o600)

    with cli.run.make_context('test-{}-ok'.format(path_kind),
                              options + recipe_arguments) as ctx:
        result = Path(ctx.params[path_kind.replace('-', '_')])
    assert result == path
    assert result.is_absolute()


def test_path_bad_permissions(runner, path_kind, recipe_arguments):
    path, options = path_options(path_kind)

    if path_kind.endswith('directory'):
        # unwritable directory
        path.mkdir()
        path.chmod(0o500)
    else:
        # unreadable file
        path.touch(mode=0o200)

    result = runner.invoke(cli.run, options + recipe_arguments,
                           standalone_mode=False)
    assert result.exception is not None
    assert isinstance(result.exception, click.BadParameter)


@pytest.mark.parametrize('pkg_cmd', ('fedpkg', 'rhpkg'))
def test_pkg_cmd_returns_valid_value(recipe_arguments, pkg_cmd):
    options = ['--pkg-cmd', pkg_cmd]
    with cli.run.make_context('test_pkg_cmd_{}_returns_value'.format(pkg_cmd),
                              options + recipe_arguments) as ctx:
        assert ctx.params['pkg_cmd'] == pkg_cmd


def test_pkg_cmd_raises_error_on_invalid_options(runner, recipe_arguments):
    options = ['--pkg-cmd', 'foo']
    result = runner.invoke(cli.run, options + recipe_arguments,
                           standalone_mode=False)
    assert result.exception is not None
    assert isinstance(result.exception, click.BadParameter)


@pytest.mark.parametrize('valid_dist',
                         ('fc', 'fc26', 'el', 'el7', 'centos', 'centos7'))
def test_dist_returns_value_on_valid_options(recipe_arguments, valid_dist):
    options = ['--dist', valid_dist]
    with cli.run.make_context('test_dist_returns_value_on_valid_options',
                              options + recipe_arguments) as ctx:
        assert isinstance(ctx.params['dist'], str)


def test_dist_raises_error_on_invalid_value(runner, recipe_arguments):
    options = ['--dist', 'fedora']
    result = runner.invoke(cli.run, options + recipe_arguments,
                           standalone_mode=False)
    assert result.exception is not None
    assert isinstance(result.exception, click.BadParameter)


def test_resume_conversion(recipe_arguments):
    """Resume is converted into integer value."""

    options = ['--resume', '42']
    with cli.run.make_context('test-resume-conversion',
                              options + recipe_arguments) as ctx:
        assert isinstance(ctx.params['resume'], int)


def test_invalid_resume(runner, recipe_arguments):

    options = ['--resume', 'start']

    result = runner.invoke(cli.run, options + recipe_arguments,
                           standalone_mode=False)
    assert result.exception is not None
    assert isinstance(result.exception, click.BadParameter)


@pytest.mark.parametrize('option,value', [
    ('branch', 'sclo7-rh-nodejs4-el7'),
    ('mock-config', 'default'),
    ('copr-repo', 'scratch-ror5'),
])
def test_simple_options(recipe_arguments, option, value):
    """Specific option values are passed unprocessed."""

    options = ['--' + option, value]
    with cli.run.make_context('test-{}-passing'.format(option),
                              options + recipe_arguments) as ctx:

        assert ctx.params[option.replace('-', '_')] == value


@pytest.mark.parametrize('help_switch', ['--help', '-h'])
def test_help_option_variants(runner, help_switch, recipe_arguments):
    """Test that both short and long version of help switch works."""

    # NOTE: recipe_arguments are necessary, both run.make_context and
    # runner.invoke break without them for some reason
    result = runner.invoke(cli.run, [help_switch] + recipe_arguments)

    assert result.exit_code == 0, result.output


@pytest.mark.parametrize('version_switch', ['--version'])
def test_version_option(runner, version_switch):
    """Test that --version option displays the version"""
    result = runner.invoke(cli.run, [version_switch])
    out = result.output.strip()

    assert result.exit_code == 0
    assert len(out.split('\n')) == 1
    assert 'version' in out


def test_choose_pkg_cmd_does_not_set(recipe_arguments):
    option_dict = {
        'pkg_cmd': 'testpkg',
    }
    cli._choose_pkg_cmd(option_dict)
    assert option_dict['pkg_cmd'] == 'testpkg'


def test_choose_pkg_cmd_sets_default_value(recipe_arguments):
    option_dict = {
        'pkg_cmd': None,
    }
    cli._choose_pkg_cmd(option_dict)
    assert option_dict['pkg_cmd'] == 'fedpkg'


@pytest.mark.parametrize('download_type', ('fedpkg', 'rhpkg'))
def test_choose_pkg_cmd_sets_download_type(recipe_arguments,
                                           download_type):
    option_dict = {
        'download': download_type,
        'pkg_cmd': None,
    }
    cli._choose_pkg_cmd(option_dict)
    assert option_dict['pkg_cmd'] == download_type


def test_choose_pkg_cmd_returns_optoin_dict_is_none():
    cli._choose_pkg_cmd(None)
    assert True


@pytest.mark.parametrize('value,exception_type', [
    (1, None),
    (1000, None),
    (-1, click.BadParameter),
])
def test_retry_sets_num_of_retries(value, exception_type, recipe_arguments):
    """Ensure proper handling of retry parameter."""

    options = ['--retry', str(value)]

    with ExitStack() as contexts:
        if exception_type:
            contexts.enter_context(pytest.raises(exception_type))

        ctx = contexts.enter_context(cli.run.make_context(
            'test-retry[{}]'.format(value),
            options + recipe_arguments,
        ))

        assert ctx.params['retry'] == value

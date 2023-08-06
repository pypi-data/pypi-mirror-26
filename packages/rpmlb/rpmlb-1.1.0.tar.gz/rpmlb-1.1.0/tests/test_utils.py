import os
import subprocess
import sys

from rpmlb import utils


def test_camelize():
    new_word = utils.camelize('foo_bar')
    assert new_word == 'FooBar'


def test_get_class():
    cls = utils.get_class('rpmlb.recipe.Recipe')
    assert cls
    cls = utils.get_class(
        'rpmlb.downloader.local.LocalDownloader'
    )
    assert cls


def test_pushd():
    original_dir = os.getcwd()
    with utils.pushd('/tmp'):
        new_dir = os.getcwd()
        assert new_dir == '/tmp'
    current_dir = os.getcwd()
    assert current_dir == original_dir


def test_run_cmd():
    result = utils.run_cmd_with_capture('echo a')
    assert isinstance(result, utils.CompletedProcess)
    assert result.returncode == 0
    assert result.stdout == b'a\n'
    assert result.stderr == b''


def test_run_cmd_exception():
    exception = False
    result_e = None
    cmd = 'ls abc'
    try:
        utils.run_cmd_with_capture(cmd)
    except subprocess.CalledProcessError as e:
        exception = True
        result_e = e

    assert exception
    assert isinstance(result_e, subprocess.CalledProcessError)
    assert result_e.cmd == cmd
    assert result_e.returncode != 0
    assert result_e.output == b''
    if sys.version_info >= (3, 5):
        assert result_e.stdout == b''
        assert b'No such file or directory' in result_e.stderr

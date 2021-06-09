#!/usr/bin/python3
#
# Basic bcachefs functionality tests.

import re
import util

def test_help():
    ret = util.run_bch(valgrind=True)

    assert ret.returncode == 1
    assert "missing command" in ret.stdout
    assert len(ret.stderr) == 0

def test_format(tmpdir):
    dev = util.device_1g(tmpdir)
    ret = util.run_bch('format', dev, valgrind=True)

    assert ret.returncode == 0
    assert len(ret.stdout) > 0
    assert len(ret.stderr) == 0

def test_fsck(tmpdir):
    dev = util.format_1g(tmpdir)

    ret = util.run_bch('fsck', dev, valgrind=True)

    assert ret.returncode == 0
    assert len(ret.stdout) > 0
    assert len(ret.stderr) == 0

def test_list(tmpdir):
    dev = util.format_1g(tmpdir)

    ret = util.run_bch('list', dev, valgrind=True)

    assert ret.returncode == 0
    assert len(ret.stderr) == 0
    assert "recovering from clean shutdown" in ret.stdout

    # Totally arbitrary, feel free to update or remove after inspecting.
    assert len(ret.stdout.splitlines()) == 97

def test_list_inodes(tmpdir):
    dev = util.format_1g(tmpdir)

    ret = util.run_bch('list', '-b', 'inodes', dev, valgrind=True)

    assert ret.returncode == 0
    assert len(ret.stderr) == 0
    assert len(ret.stdout.splitlines()) == (2 + 2) # 2 inodes on clean format

def test_list_dirent(tmpdir):
    dev = util.format_1g(tmpdir)

    ret = util.run_bch('list', '-b', 'dirents', dev, valgrind=True)

    assert ret.returncode == 0
    assert len(ret.stderr) == 0
    assert len(ret.stdout.splitlines()) == (2 + 1) # 1 dirent

    # Example:
    # u64s 8 type dirent 4096:2449855786607753081
    # snap 0 len 0 ver 0: lost+found -> 4097
    last = ret.stdout.splitlines()[-1]
    assert re.match(r'^.*type dirent.*: lost\+found ->.*$', last)

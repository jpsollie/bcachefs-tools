#!/usr/bin/python3
#
# Tests of the fuse mount functionality.

import pytest
import os
import util

pytestmark = pytest.mark.skipif(
    not util.have_fuse(), reason="bcachefs not built with fuse support.")

def test_mount(bfuse):
    bfuse.mount()
    bfuse.unmount()
    bfuse.verify()

@pytest.mark.skipif(util.ENABLE_VALGRIND, reason="test broken")
def test_remount(bfuse):
    bfuse.mount()
    bfuse.unmount()
    bfuse.mount()
    bfuse.unmount()
    bfuse.verify()

def test_lostfound(bfuse):
    bfuse.mount()

    lf = bfuse.mnt / "lost+found"
    assert lf.is_dir()

    st = lf.stat()
    assert st.st_mode == 0o40700

    bfuse.unmount()
    bfuse.verify()

def test_create(bfuse):
    bfuse.mount()

    path = bfuse.mnt / "file"

    with util.Timestamp() as ts:
        fd = os.open(path, os.O_CREAT, 0o700)

    assert fd >= 0

    os.close(fd)
    assert path.is_file()

    # Verify file.
    st = path.stat()
    assert st.st_mode == 0o100700
    assert st.st_mtime == st.st_ctime
    assert st.st_mtime == st.st_atime
    assert ts.contains(st.st_mtime)

    # Verify dir.
    dst = bfuse.mnt.stat()
    assert dst.st_mtime == dst.st_ctime
    assert ts.contains(dst.st_mtime)

    bfuse.unmount()
    bfuse.verify()

def test_mkdir(bfuse):
    bfuse.mount()

    path = bfuse.mnt / "dir"

    with util.Timestamp() as ts:
        os.mkdir(path, 0o700)

    assert path.is_dir()

    # Verify child.
    st = path.stat()
    assert st.st_mode == 0o40700
    assert st.st_mtime == st.st_ctime
    assert st.st_mtime == st.st_atime
    assert ts.contains(st.st_mtime)

    # Verify parent.
    dst = bfuse.mnt.stat()
    assert dst.st_mtime == dst.st_ctime
    assert ts.contains(dst.st_mtime)

    bfuse.unmount()
    bfuse.verify()

def test_unlink(bfuse):
    bfuse.mount()

    path = bfuse.mnt / "file"
    path.touch(mode=0o600, exist_ok=False)

    with util.Timestamp() as ts:
        os.unlink(path)

    assert not path.exists()

    # Verify dir.
    dst = bfuse.mnt.stat()
    assert dst.st_mtime == dst.st_ctime
    assert ts.contains(dst.st_mtime)

    bfuse.unmount()
    bfuse.verify()

def test_rmdir(bfuse):
    bfuse.mount()

    path = bfuse.mnt / "dir"
    path.mkdir(mode=0o700, exist_ok=False)

    with util.Timestamp() as ts:
        os.rmdir(path)

    assert not path.exists()

    # Verify dir.
    dst = bfuse.mnt.stat()
    assert dst.st_mtime == dst.st_ctime
    assert ts.contains(dst.st_mtime)

    bfuse.unmount()
    bfuse.verify()

def test_rename(bfuse):
    bfuse.mount()

    srcdir = bfuse.mnt

    path = srcdir / "file"
    path.touch(mode=0o600, exist_ok=False)

    destdir = srcdir / "dir"
    destdir.mkdir(mode=0o700, exist_ok=False)

    destpath = destdir / "file"

    path_pre_st = path.stat()

    with util.Timestamp() as ts:
        os.rename(path, destpath)

    assert not path.exists()
    assert destpath.is_file()

    # Verify dirs.
    src_st = srcdir.stat()
    assert src_st.st_mtime == src_st.st_ctime
    assert ts.contains(src_st.st_mtime)

    dest_st = destdir.stat()
    assert dest_st.st_mtime == dest_st.st_ctime
    assert ts.contains(dest_st.st_mtime)

    # Verify file.
    path_post_st = destpath.stat()
    assert path_post_st.st_mtime == path_pre_st.st_mtime
    assert path_post_st.st_atime == path_pre_st.st_atime
    assert ts.contains(path_post_st.st_ctime)

    bfuse.unmount()
    bfuse.verify()

def test_link(bfuse):
    bfuse.mount()

    srcdir = bfuse.mnt

    path = srcdir / "file"
    path.touch(mode=0o600, exist_ok=False)

    destdir = srcdir / "dir"
    destdir.mkdir(mode=0o700, exist_ok=False)

    destpath = destdir / "file"

    path_pre_st = path.stat()
    srcdir_pre_st = srcdir.stat()

    with util.Timestamp() as ts:
        os.link(path, destpath)

    assert path.exists()
    assert destpath.is_file()

    # Verify source dir is unchanged.
    srcdir_post_st = srcdir.stat()
    assert srcdir_pre_st == srcdir_post_st

    # Verify dest dir.
    destdir_st = destdir.stat()
    assert destdir_st.st_mtime == destdir_st.st_ctime
    assert ts.contains(destdir_st.st_mtime)

    # Verify file.
    path_post_st = path.stat()
    destpath_post_st = destpath.stat()
    assert path_post_st == destpath_post_st

    assert path_post_st.st_mtime == path_pre_st.st_mtime
    assert path_post_st.st_atime == path_pre_st.st_atime
    assert ts.contains(path_post_st.st_ctime)

    bfuse.unmount()
    bfuse.verify()

def test_write(bfuse):
    bfuse.mount()

    path = bfuse.mnt / "file"
    path.touch(mode=0o600, exist_ok=False)

    pre_st = path.stat()

    fd = os.open(path, os.O_WRONLY)
    assert fd >= 0

    with util.Timestamp() as ts:
        written = os.write(fd, b'test')

    os.close(fd)

    assert written == 4

    post_st = path.stat()
    assert post_st.st_atime == pre_st.st_atime
    assert post_st.st_mtime == post_st.st_ctime
    assert ts.contains(post_st.st_mtime)

    assert path.read_bytes() == b'test'

    bfuse.unmount()
    bfuse.verify()

import grp
import os
import pwd
import shutil
import stat
from pathlib import Path

import pytest

import distrax.utils.fileio as fileio

TEST_FOLDER = "TEST_FOLDER"
TEST_SUB_FOLDER = TEST_FOLDER + "/" + TEST_FOLDER
TEST_FILE = "TEST_FILE.txt"
TEST_FILE2 = "TEST_FILE2.txt"
NON_EXISTENT_FILE = "NON_EXISTENT_FILE.txt"
TEST_USER = "test_python_user"
TEST_GRP = "test_python_group"


@pytest.fixture()
def folder_resource():
    """
    Creates a folder and removes after testing
    """
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)
    os.mkdir(TEST_FOLDER)
    yield "text_file_resource"
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)


@pytest.fixture()
def sub_folder_file_resource():
    """
    Creates a folder and removes after testing
    """
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)
    os.mkdir(TEST_FOLDER)
    os.mkdir(TEST_SUB_FOLDER)
    open(TEST_SUB_FOLDER + "/" + TEST_FILE, "w").close()
    yield "text_file_resource"
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)


@pytest.fixture()
def file_resource():
    """
    Creates a textfile and removes after testing
    """
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    open(TEST_FILE, "w").close()
    yield "text_file_resource"
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


@pytest.fixture()
def files_resource():
    """
    Create text files with hi inside
    """
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)
    os.mkdir(TEST_FOLDER)
    with open(TEST_FOLDER + "/" + TEST_FILE, "w") as f:
        f.write("hi")
        f.close()
    with open(TEST_FOLDER + "/" + TEST_FILE2, "w") as f:
        f.write("hi")
        f.close()
    yield "files_resource"
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)


class TestFileIO:
    """
    Tests functions within FileIO
    """

    def test_create_create_dir(self):
        mode = 777
        test = fileio.create_dir(TEST_FOLDER, mode)
        assert test is True
        assert stat.S_IMODE(os.lstat(TEST_FOLDER).st_mode) == mode
        # Create folder that already exists
        test = fileio.create_dir(TEST_FOLDER, mode)
        assert test is False
        os.removedirs(TEST_FOLDER)

    def test_remove_dir(self, folder_resource):
        test = fileio.remove_dir(TEST_FOLDER)
        assert test is True
        test = fileio.remove_dir(TEST_FOLDER)
        assert test is False

    def test_copy_file(self, folder_resource, file_resource):
        test = fileio.copy_file(TEST_FILE, TEST_FOLDER)
        assert test is True
        assert os.path.exists(TEST_FILE)
        assert os.path.exists(TEST_FOLDER + "/" + TEST_FILE)
        test = fileio.copy_file(NON_EXISTENT_FILE, TEST_FOLDER)
        assert test is False

    def test_remove_file(self, file_resource):
        test = fileio.remove_file(TEST_FILE)
        assert test is True
        test = fileio.remove_file(TEST_FILE)
        assert test is False

    def test_change_ownership(self, file_resource):
        if os.geteuid() != 0:
            pytest.fail("Need to run as ROOT to pass this test")
        try:
            pwd.getpwnam(TEST_USER)
            grp.getgrnam(TEST_GRP)
            current_user = Path(TEST_FILE).owner()
            current_grp = Path(TEST_FILE).group()
            assert current_user != TEST_USER
            assert current_grp != TEST_GRP
            test = fileio.change_ownership(TEST_FILE, TEST_USER, TEST_GRP)
            assert test is True
            assert Path(TEST_FILE).owner() == TEST_USER
            assert Path(TEST_FILE).group() == TEST_GRP
            test = fileio.change_ownership(NON_EXISTENT_FILE, TEST_USER, TEST_GRP)
            assert test is False
        except KeyError:
            pytest.fail(
                "\nExpecting TEST_USER (test_python_user) and "
                + "TEST_GRP (test_python_group) "
                + "This test will auto fail if they are not present. "
                + "This requires being run in root.\n",
                "",
            )

    def test_recursive_change_ownership(self, sub_folder_file_resource):
        if os.geteuid() != 0:
            pytest.fail("Need to run as ROOT to pass this test")
        try:
            pwd.getpwnam(TEST_USER)
            grp.getgrnam(TEST_GRP)
            current_user = Path(TEST_FOLDER).owner()
            current_grp = Path(TEST_FOLDER).group()
            assert current_user != TEST_USER
            assert current_grp != TEST_GRP
            current_sub_user = Path(TEST_SUB_FOLDER).owner()
            current_sub_grp = Path(TEST_SUB_FOLDER).group()
            assert current_sub_user != TEST_USER
            assert current_sub_grp != TEST_GRP
            test = fileio.recursive_change_ownership(TEST_FOLDER, TEST_USER, TEST_GRP)
            assert test is True
            assert Path(TEST_FOLDER).owner() == TEST_USER
            assert Path(TEST_FOLDER).group() == TEST_GRP
            assert Path(TEST_SUB_FOLDER).owner() == TEST_USER
            assert Path(TEST_SUB_FOLDER).group() == TEST_GRP
            test = fileio.recursive_change_ownership(
                NON_EXISTENT_FILE, TEST_USER, TEST_GRP
            )
            assert test is False
        except KeyError:
            pytest.fail(
                "\nExpecting TEST_USER (test_python_user) and "
                + "TEST_GRP (test_python_group) "
                + "This test will auto fail if they are not present. "
                + "This requires being run in root.\n",
                "",
            )

    def test_change_permissions(self, file_resource):
        test_file_mode = oct(os.stat(TEST_FILE).st_mode & 0o777)
        fileio.change_permissions(TEST_FILE, 0o777)
        assert test_file_mode != oct(os.stat(TEST_FILE).st_mode & 0o777)
        assert fileio.change_permissions(NON_EXISTENT_FILE, 0o777) is False

    def test_recursive_change_permissions(self, sub_folder_file_resource):
        test_folder_mode = oct(os.stat(TEST_FOLDER).st_mode & 0o777)
        test_subfolder_mode = oct(os.stat(TEST_SUB_FOLDER).st_mode & 0o777)
        test_file_mode = oct(os.stat(f"{TEST_SUB_FOLDER}/{TEST_FILE}").st_mode & 0o777)
        fileio.recursive_change_permissions(TEST_FOLDER, 0o777)
        assert test_file_mode != oct(
            os.stat(f"{TEST_SUB_FOLDER}/{TEST_FILE}").st_mode & 0o777
        )
        assert test_subfolder_mode != oct(os.stat(TEST_SUB_FOLDER).st_mode & 0o777)
        assert test_folder_mode != oct(os.stat(TEST_FOLDER).st_mode & 0o777)
        assert fileio.recursive_change_permissions(NON_EXISTENT_FILE, 0o777) is False

    def test_append_file_in_folder(self, files_resource):
        fileio.append_file_in_folder(TEST_FOLDER, TEST_FILE, [TEST_FILE2])
        with open(TEST_FOLDER + "/" + TEST_FILE) as f:
            assert f.readline() == "hi\n"
            assert f.readline() == "hi"

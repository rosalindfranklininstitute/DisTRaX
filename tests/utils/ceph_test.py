import distrax.utils.ceph as ceph
import pytest
import os
import shutil

TEST_FOLDER = "TEST_FOLDER"


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


class TestCeph:
    """
    Tests functions within Ceph
    """

    def test_generate_auth_key(self):
        key1 = ceph.generate_auth_key()
        key2 = ceph.generate_auth_key()
        assert len(key1) == 40
        assert len(key2) == 40
        assert key1 != key2

    def test_create_keyring(self, folder_resource):
        ceph.create_keyring(TEST_FOLDER, "mon.", {"caps mon": "allow *"})
        with open(f"{TEST_FOLDER}/{ceph.MON_KEYRING}") as key:
            assert key.readline() == "[mon.]\n"
            assert key.readline()  # Key-line which is unknown
            assert key.readline() == "caps mon = allow *\n"

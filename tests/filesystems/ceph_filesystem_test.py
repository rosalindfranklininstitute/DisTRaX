from distrax.filesystems.abstract_filesystem import AbstractFilesystem
from distrax.filesystems.ceph_filesystem import CephFilesystem


class TestCephFilesytem:

    """
    Testing CephFilesystem
    """

    def test_is_subclass_of_abstract_filesystem(self):
        assert issubclass(CephFilesystem, AbstractFilesystem)

    def test_instance_of_abstract_filesystem(self):
        assert isinstance(CephFilesystem(), AbstractFilesystem)

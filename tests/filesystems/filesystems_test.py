import distrax.filesystems as filesystems
from distrax.filesystems.abstract_filesystem import AbstractFilesystem


class TestFilesystems:
    """
    Testing that the Filesystems created are subclasses and instances
    of the AbstractFilesystem
    """

    def test_is_subclass_of_abstract_filesystem(self):
        for filesystem in filesystems.AVAILABLE:
            filesystems.set_filesystem(filesystem)
            fs = filesystems.get_filesystem(filesystem)
            assert issubclass(fs.FILESYSTEM, AbstractFilesystem)

    def test_instance_of_abstract_filesystem(self):
        for filesystem in filesystems.AVAILABLE:
            filesystems.set_filesystem(filesystem)
            fs = filesystems.get_filesystem(filesystem)
            assert isinstance(fs.FILESYSTEM(), AbstractFilesystem)

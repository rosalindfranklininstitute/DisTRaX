from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class AbstractFilesystem(Protocol):
    """An interface for Filesystem Classes.

    This is a Template for the mounting and remove of filesystems

    This is designed such plugins of the Filesystem can be made easily.
    The only methods publicly visible to the user should be mount_filesystem and
    unmount_filesystem
    """

    def mount_filesystem(self) -> None:
        """Mount the filesystem."""
        ...

    def unmount_filesystem(self) -> None:
        """Unmount the filesystem."""
        ...

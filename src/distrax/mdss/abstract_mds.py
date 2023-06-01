from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class AbstractMDS(Protocol):
    """An interface for MDS Classes.

    An MDS is the cluster filesystem daemon, this is required for a filesystem to be
    created. It is used to manage the file system namespace and coordinating access to
    the storage for read and write.

    This is designed such plugins of the MDS can be made easily.
    The only methods publicly visible to the user should be create_mds and remove_mds
    """

    def create_mds(self) -> None:
        """Create the Metadata Server node."""
        ...

    def remove_mds(self) -> None:
        """Remove the Metadata Server node."""
        ...

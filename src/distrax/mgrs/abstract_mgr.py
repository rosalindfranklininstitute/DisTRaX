from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class AbstractMGR(Protocol):
    """
    An interface for MON Classes

    A MGR is the cluster manager daemon, this is often used to maintain cluster health,
    and make sure that all the parts of the cluster can communicate.

    This is designed such plugins of the MGR can be made easily.
    The only methods publicly visible to the user should be create_mgr and remove_mgr
    """

    def create_mgr(self) -> None:
        """
        Create the manager node
        """
        ...

    def remove_mgr(self) -> None:
        """
        Remove the manager node
        """
        ...

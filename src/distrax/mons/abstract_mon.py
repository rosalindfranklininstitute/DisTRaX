from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class AbstractMON(Protocol):
    """
    An interface for MON Classes

    A MON is the cluster monitor daemon, this is often used to maintain cluster health,
    and make sure that all the parts of the cluster can communicate.

    This is designed such plugins of the MON can be made easily.
    The only methods publicly visible to the user should be create_mon and remove_mon
    """

    def create_mon(self, interface: str) -> None:
        """
        Create the monitor node

        Args:
            interface: the network interface the cluster will be using.

        """
        ...

    def remove_mon(self) -> None:
        """
        Remove the monitor node
        """
        ...

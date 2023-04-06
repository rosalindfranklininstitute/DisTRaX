import abc


class AbstractMON(metaclass=abc.ABCMeta):
    """
    An interface for MON Classes

    A MON is the cluster monitor daemon, this is often used to maintain cluster health,
    and make sure that all the parts of the cluster can communicate.

    This is designed such plugins of the MON can be made easily.
    The only methods publicly visible to the user should be create_mon and remove_mon
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """
        Check if the functions are present and implemented in a subclass
        This ensures that the abstract class is adhered to.
        Args:
            subclass: The class to check

        Returns:
            True if functions are present, otherwise False

        """
        return (
            hasattr(subclass, "create_mon")
            and callable(subclass.create_mon)
            and hasattr(subclass, "remove_mon")
            and callable(subclass.remove_mon)
            or NotImplemented
        )

    @abc.abstractmethod
    def create_mon(self, interface: str) -> bool:
        """
        Create the monitor node

        Args:
            interface: the network interface the cluster will be using.

        Raises:
            NotImplementedError: until implemented

        Returns:
            True if mon is created, otherwise False
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_mon(self) -> bool:
        """
        Remove the monitor node

        Stop and Disable the monitor node

        Raises:
            NotImplementedError: until implemented

        Returns:
            True if mon is removed, otherwise False
        """
        raise NotImplementedError

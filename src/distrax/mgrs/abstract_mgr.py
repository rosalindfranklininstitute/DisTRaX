import abc


class AbstractMGR(metaclass=abc.ABCMeta):
    """
    An interface for MON Classes

    A MGR is the cluster manager daemon, this is often used to maintain cluster health,
    and make sure that all the parts of the cluster can communicate.

    This is designed such plugins of the MGR can be made easily.
    The only methods publicly visible to the user should be create_mgr and remove_mgr
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
    def create_mgr(self, folder: str) -> bool:
        """
        Create the manager node

        Args:
            folder: The folder to place files created

        Raises:
            NotImplementedError: until implemented

        Returns:
            True if mon is created, otherwise False
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_mgr(self, folder: str) -> bool:
        """
        Remove the manager node

        Stop and Disable the manager node

        Args:
            folder: The folder to remove that contains the files created

        Raises:
            NotImplementedError: until implemented

        Returns:
            True if mon is removed, otherwise False
        """
        raise NotImplementedError

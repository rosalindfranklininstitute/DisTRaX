import abc
from typing import List


class AbstractOSD(metaclass=abc.ABCMeta):
    """
    An interface for OSD Classes

    An Object Storage Device, to be created on top of a block device

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
            hasattr(subclass, "create_osds")
            and callable(subclass.create_osds)
            and hasattr(subclass, "remove_osds")
            and callable(subclass.remove_osds)
            or NotImplemented
        )

    @abc.abstractmethod
    def create_osds(self, devices: List[str]):
        """
        Create the OSD devices
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_osds(self, devices: List[str]):
        """
        Remove the block devices created
        """
        raise NotImplementedError

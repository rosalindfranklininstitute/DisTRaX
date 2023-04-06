import abc


class AbstractDevice(metaclass=abc.ABCMeta):
    """
    An interface for Device Classes

    A Device is a Block Device that will store the Object Storage Device.
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
            hasattr(subclass, "create_device")
            and callable(subclass.create_device)
            and hasattr(subclass, "remove_device")
            and callable(subclass.remove_device)
            or NotImplemented
        )

    @abc.abstractmethod
    def create_device(self, size: int, number: int = 1):
        """
        Create the block storage device
        Args:
            size(int): The size of the blocks' device in GibiBytes i.e. 1 would be 1GiB
            number(int): Number of block devices to create, i.e. 4 will create 4 devices
                        of the size stated
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_device(self):
        """
        Remove the block devices created
        """
        raise NotImplementedError

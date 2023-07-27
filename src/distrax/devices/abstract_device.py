from typing import Protocol, runtime_checkable


@runtime_checkable
class AbstractDevice(Protocol):
    """An interface for Device Classes.

    A Device is a Block Device that will store the Object Storage Device.
    """

    def create_device(self, size: int, number: int = 1) -> None:
        """Create the block storage device.

        Args:
            size: The size of the blocks' device in GibiBytes i.e. 1 would be 1GiB
            number: Number of block devices to create, i.e. 4 will create 4 devices
                        of the size stated
        """
        ...

    def remove_device(self) -> None:
        """Remove the block devices created."""
        ...

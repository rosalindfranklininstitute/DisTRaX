from typing_extensions import Protocol, runtime_checkable
from typing import List


@runtime_checkable
class AbstractOSD(Protocol):
    """
    An interface for OSD Classes

    An Object Storage Device, to be created on top of a block device

    """

    def create_osds(self, devices: List[str]) -> None:
        """
        Create the OSD devices
        """
        ...

    def remove_osds(self, devices: List[str]) -> None:
        """
        Remove the block devices created
        """
        ...

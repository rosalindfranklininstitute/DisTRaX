from typing import List

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class AbstractOSD(Protocol):
    """An interface for OSD Classes.

    Outlines the methods required for OSD classes, for an OSD class to be functional
    it must implement `create_osds` and `remove_osds` in the method stated here.
    """

    def create_osds(self, devices: List[str]) -> None:
        """Create the OSD devices.

        Args:
            devices: A list of block devices files names,
                e.g. /dev/nvme0n1p1 or /dev/ram0
        """
        ...

    def remove_osds(self, devices: List[str]) -> None:
        """Remove the block devices created.

        Args:
            devices: A list of block devices files names,
                e.g. /dev/nvme0n1p1 or /dev/ram0
        """
        ...

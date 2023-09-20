from typing import List, Protocol, runtime_checkable


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

    def is_osd_ready(self, num_up_and_in: int) -> bool:
        """Check if the OSDs are ready.

        Args:
            num_up_and_in: The number of OSDS expected to be up and running

        Returns:
            True when the number of up and in match stated requirment.

        Examples:
            >>> osd.osd_ready()
                True

        """
        ...

    def remove_osds(self) -> None:
        """Remove the OSDs created."""
        ...

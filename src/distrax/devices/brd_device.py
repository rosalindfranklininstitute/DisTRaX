import os
import subprocess

from distrax.exceptions.exceptions import DeviceCreationError, NotEnoughMemoryError
from distrax.utils.system import free_memory


class BRDDevice:
    """BRDDevice class this allows for the creation and removal of the RAM block device.

    It is important to note that this device uses system memory
    and the block devices will be found at /dev/ram{number}

    Examples:
        >>> device = BRDDevice()
    """

    @staticmethod
    def create_device(size: int, number: int = 1) -> None:
        """Create BRD Block Device.

        Args:
            size: number representing a GiB, i.e 4 would mean 4GiB
            number: Number of block devices to create, i.e. 4 will create 4 devices
                        of the size stated

        Raises:
            NotEnoughMemoryError(): If the amount of memory requested is higher
                                than the memory available
            DeviceCreationError(): If the creation device fails this either to
                                existing device or another reason.

        Returns:
            Creates n blocks devices of the size stated.

        Examples:
            >>> device.create_device(1, 10)
            # Creates 10 1Gib block devices using system memory
        """
        size = size * 1024**2  # for BRD the size needs to be in KiB
        free_mem = free_memory()
        if size * number > free_mem:
            raise NotEnoughMemoryError(
                f"{number} Devices of {size}KiB totaling {number * size}KiB requested "
                f"when only {free_mem}KiB available, please reduce the number of "
                f"devices or the size of the device"
            )
        if os.path.exists("/dev/ram0"):
            raise DeviceCreationError(
                "BRD Ram Blocks already exists therefore new block device cannot be "
                "created, please remove previous RAM block device before continuing"
            )
        return_code = subprocess.run(
            ["modprobe", "brd", f"rd_size={size}", "max_part=1", f"rd_nr={number}"]
        ).returncode
        if return_code != 0:
            raise DeviceCreationError(
                "Device creation failed, please investigate further before running "
                "DisTRaX again"
            )

    @staticmethod
    def remove_device() -> None:
        """Removes the BRD device from the systems.

        Examples:
            >>> device.remove_device()
            # Removes the BRD block device from the system.

        """
        subprocess.run(
            ["rmmod", "brd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

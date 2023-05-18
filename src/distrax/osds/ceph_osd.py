import glob
import subprocess
from typing import List

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.system as system


class CephOSD:
    """Class for the creation and removal of Ceph OSDs.

    To read more about the Ceph OSD please see:
    https://docs.ceph.com/en/latest/glossary/#term-Ceph-OSD

    Examples:
        >>> osd = CephOSD()

        >>> osd = CephOSD(folder="distrax")
    """

    def __init__(self, folder: str = "ceph"):
        """Initialise the CephOSD object.

        Args:
            folder: the place to place the keys of the ceph system
        """
        self.folder = folder

    def create_osds(self, devices: List[str]) -> None:
        """Create the OSDs devices.

        Args:
            devices: The device names to turn into OSDs.

        Examples:
            >>> osd.create_osds(["/dev/ram0", "/dev/ram1"])
        """
        # Create needed directories for OSDs to run on the system
        fileio.create_dir(ceph.VAR_BOOTSTRAP_OSD, 0o755)
        fileio.recursive_change_ownership(ceph.VAR_BOOTSTRAP_OSD, "ceph", "ceph")
        fileio.create_dir(ceph.VAR_OSD, 0o755)
        fileio.recursive_change_ownership(ceph.VAR_OSD, "ceph", "ceph")

        # Copy OSDs files to ETC Ceph
        fileio.copy_file(
            f"{self.folder}/{ceph.CONFIG_FILE}", f"{ceph.ETC_CEPH}/{ceph.CONFIG_FILE}"
        )
        fileio.copy_file(
            f"{self.folder}/{ceph.ADMIN_KEYRING}",
            f"{ceph.ETC_CEPH}/{ceph.ADMIN_KEYRING}",
        )

        fileio.copy_file(
            f"{self.folder}/{ceph.OSD_KEYRING}", f"{ceph.ETC_CEPH}/ceph.keyring"
        )
        # Copy OSDs files to VAR Ceph
        fileio.copy_file(
            f"{self.folder}/{ceph.OSD_KEYRING}",
            f"{ceph.VAR_BOOTSTRAP_OSD}/ceph.keyring",
        )
        # Create the OSDs using ceph-volume
        for device in devices:
            subprocess.run(["ceph-volume", "lvm", "create", "--data", device])

    def remove_osds(self, devices: List[str]) -> None:
        """Remove the OSDs devices from the system.

        Args:
            devices: The device names to turn into OSDs

        Examples:
            >>> osd.remove_osds(["/dev/ram0", "/dev/ram1"])
        """
        # Get OSD_ids from the host system
        osd_ids = glob.glob(f"{ceph.VAR_OSD_ID}*")
        # Set OSDs to out to ensure safe removal
        for osd_id in osd_ids:
            osd_id = osd_id.strip(ceph.VAR_OSD_ID)
            subprocess.run(["ceph", "osd", "out", str(osd_id)])
            system.stop_service(f"ceph-osd@{osd_id}")
            system.stop_service(f"var-lib-ceph-osd-ceph\\x2d{osd_id}.mount")
        # Stop OSDs service
        system.stop_service("ceph-osd.target")
        system.disable_service("ceph-osd.target")
        # Remove ceph and clean devices
        for device in devices:
            subprocess.run(["ceph-volume", "lvm", "zap", "--destroy", device])
        # Get ceph-volume services
        osd_services = glob.glob(
            "/etc/systemd/system/multi-user.target.wants/ceph-volume@lvm-*"
        )
        # remove ceph-volume services
        for osd_service in osd_services:
            fileio.remove_file(osd_service)
        system.stop_service("system-ceph\\x2dosd.slice")
        fileio.remove_dir(ceph.VAR_BOOTSTRAP_OSD)
        fileio.remove_dir(ceph.VAR_OSD)

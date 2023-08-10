import glob
import logging
import subprocess
import time
from typing import List

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.system as system
from distrax.osds import OSD


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
        fileio.create_dir(ceph.VAR_BOOTSTRAP_OSD, 755, admin=True)
        fileio.create_dir(ceph.VAR_OSD, 755, admin=True)

        # Copy OSDs files to ETC Ceph
        fileio.copy_file(
            f"{self.folder}/{ceph.CONFIG_FILE}",
            f"{ceph.ETC_CEPH}/{ceph.CONFIG_FILE}",
            admin=True,
        )
        fileio.copy_file(
            f"{self.folder}/{ceph.ADMIN_KEYRING}",
            f"{ceph.ETC_CEPH}/{ceph.ADMIN_KEYRING}",
            admin=True,
        )

        fileio.copy_file(
            f"{self.folder}/{ceph.OSD_KEYRING}",
            f"{ceph.ETC_CEPH}/ceph.keyring",
            admin=True,
        )
        # Copy OSDs files to VAR Ceph
        fileio.copy_file(
            f"{self.folder}/{ceph.OSD_KEYRING}",
            f"{ceph.VAR_BOOTSTRAP_OSD}/ceph.keyring",
            admin=True,
        )
        # Create the OSDs using ceph-volume
        for device in devices:
            subprocess.run(["ceph-volume", "lvm", "create", "--data", device])

    def remove_osds(self) -> None:
        """Remove the OSDs devices from the system.

        Examples:
            >>> osd.remove_osds()
        """
        # Get OSD_ids from the host system
        osd_ids = glob.glob(f"{ceph.VAR_OSD_ID}*")
        # Set OSDs to out to ensure safe removal
        for osd_id in osd_ids:
            osd_id = osd_id.strip(ceph.VAR_OSD_ID)
            subprocess.run(
                ["ceph", "osd", "out", str(osd_id), "--connect-timeout", "5"]
            )
            # Wait for the osd to be set to out
            time.sleep(1)
            # Stop services
            system.stop_service(f"ceph-osd@{osd_id}")
            system.stop_service(f"var-lib-ceph-osd-ceph\\x2d{osd_id}.mount")
        # Stop OSDs service
        system.stop_service("ceph-osd.target")
        system.disable_service("ceph-osd.target")
        # Remove ceph and clean devices
        pvs_process = subprocess.run(
            ["sudo", "pvs", "--separator", ",", "-o", "pv_name,vg_name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        pvs_output = pvs_process.stdout.decode("utf-8")
        pvs_output_lst = pvs_output.replace(" ", "").splitlines()
        for pv in pvs_output_lst:
            pvs = pv.split(",")  # PV, VG
            if pvs[1][:4] == "ceph":
                subprocess.run(
                    ["sudo", "ceph-volume", "lvm", "zap", "--destroy", pv[0]],
                )
        # Get ceph-volume services
        osd_services = glob.glob(
            "/etc/systemd/system/multi-user.target.wants/ceph-volume@lvm-*"
        )
        # remove ceph-volume services
        for osd_service in osd_services:
            fileio.remove_file(osd_service, admin=True)
        for osd_id in osd_ids:
            osd_id = osd_id.strip(ceph.VAR_OSD_ID)
            fileio.remove_file(f"{ceph.VAR_RUN}osd.{osd_id}.asok", admin=True)
        system.stop_service("system-ceph\\x2dosd.slice")
        system.stop_service("system-ceph\\x2dvolume.slice")
        fileio.remove_dir(ceph.VAR_BOOTSTRAP_OSD, admin=True)
        fileio.remove_dir(ceph.VAR_OSD, admin=True)


_osd = OSD("ceph", CephOSD)

import glob
import json
import logging
import subprocess
import time
from typing import List

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.system as system
from distrax.osds import OSD

logger = logging.getLogger(__name__)


class CephOSD:
    """Class for the creation and removal of Ceph OSDs.

    To read more about the Ceph OSD please see:
    https://docs.ceph.com/en/latest/glossary/#term-Ceph-OSD

    Examples:
        >>> osd = CephOSD()

        >>> osd = CephOSD(folder="distrax")
    """

    def __init__(
        self, folder: str = "ceph", system_timeout: int = 60, ceph_timeout: int = 5
    ):
        """Initialise the CephOSD object.

        Args:
            folder: the place to place the keys of the ceph system.
            system_timeout: The amount of time before a timeout for system actions,
            this defaulted to 60 seconds.
            ceph_timeout: The amount of time a ceph command can run before timeout.
        """
        self.folder = folder
        self.system_timeout = system_timeout
        self.ceph_timeout = str(ceph_timeout)

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
            subprocess.run(
                ["sudo", "ceph-volume", "lvm", "create", "--data", device],
            )
            logger.info(f"Created {device} OSD")

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
        status_process = subprocess.run(
            [
                "ceph",
                "osd",
                "stat",
                "--format=json",
                "--connect-timeout",
                self.ceph_timeout,
            ],
            stdout=subprocess.PIPE,
        )
        status = dict(json.loads(status_process.stdout))
        """{'epoch': 1, 'num_osds': 5, 'num_up_osds': 5, 'osd_up_since': 1,
            'num_in_osds': 5, 'osd_in_since': 1, 'num_remapped_pgs': 0}"""
        if (
            status["num_up_osds"] == num_up_and_in
            and status["num_in_osds"] == num_up_and_in
        ):
            return True
        return False

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
                [
                    "ceph",
                    "osd",
                    "out",
                    str(osd_id),
                    "--connect-timeout",
                    self.ceph_timeout,
                ]
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
                remove_osd_process = subprocess.run(
                    ["sudo", "ceph-volume", "lvm", "zap", "--destroy", pvs[0]],
                )
                while remove_osd_process.returncode != 0:
                    time.sleep(1)
                    remove_osd_process = subprocess.run(
                        ["sudo", "ceph-volume", "lvm", "zap", "--destroy", pvs[0]],
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

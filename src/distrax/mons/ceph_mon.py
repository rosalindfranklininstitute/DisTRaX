import configparser
import os
import subprocess
import uuid

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.network as network
import distrax.utils.system as system
from distrax.mons import MON


class CephMON:
    """Ceph Monitor Class.

    This class contains all the methods required to create and remove a Ceph Monitor

    To read more about the Ceph Monitor please see:
    https://docs.ceph.com/en/latest/glossary/#term-Ceph-Monitor

    Examples:
        >>> mon = CephMON()

        >>> mon = CephMON(folder="distrax")

    """

    def __init__(self, folder: str = "ceph") -> None:
        """Initialise the CephMON object.

        Args:
            folder: the location to store the keys of the ceph system

        Examples:
            >>> mon = CephMON()
        """
        self.hostname = network.hostname()
        self.fsid: str = ""
        self.ip: str = ""
        self.ip_netmask: str = ""
        self.folder = folder

    def create_mon(self, interface: str) -> None:
        """Create the Ceph Monitor daemon.

        Args:
            interface: the network interface the cluster will be using.

        Examples:
            >>> mon.create_mon("lo")
        """
        # Get system details
        self.fsid = str(uuid.uuid4().hex)
        self.ip = network.ip_address_from_network_interface(interface)
        self.ip_netmask = network.ip_with_netmask(self.ip)
        # Create required self.folders
        fileio.create_dir(f"{ceph.VAR_MON}{self.hostname}", 0o755)
        fileio.create_dir(self.folder, 0o775)
        # Write config
        self._write_config_file()
        fileio.copy_file(
            f"{self.folder}/{ceph.CONFIG_FILE}", f"{ceph.ETC_CEPH}/{ceph.CONFIG_FILE}"
        )
        # Create keys
        ceph.create_mon_key(self.folder)
        ceph.create_admin_key(self.folder)
        ceph.create_osd_key(self.folder)
        fileio.append_file_in_folder(
            self.folder, ceph.MON_KEYRING, [ceph.ADMIN_KEYRING, ceph.OSD_KEYRING]
        )
        # Create Monmap
        self._create_monmap()
        fileio.recursive_change_ownership(self.folder, os.getlogin(), os.getlogin())
        # Create Cluster
        self._create_cluster()
        # Copy files
        fileio.copy_file(
            f"{self.folder}/{ceph.MON_KEYRING}",
            f"{ceph.VAR_MON}{self.hostname}/keyring",
        )
        fileio.recursive_change_ownership(
            f"{ceph.VAR_MON}{self.hostname}", "ceph", "ceph"
        )
        fileio.copy_file(
            f"{self.folder}/{ceph.ADMIN_KEYRING}",
            f"{ceph.ETC_CEPH}/{ceph.ADMIN_KEYRING}",
        )

        # Start Monitor
        system.start_service(f"ceph-mon@{self.hostname}")
        subprocess.run(["ceph", "mon", "enable-msgr2"])

    def _create_cluster(self) -> None:
        """Create the Ceph Cluster with the monitor node."""
        subprocess.run(
            [
                "ceph-mon",
                "--cluster",
                "ceph",
                "--mkfs",
                "-i",
                self.hostname,
                "--monmap",
                f"{self.folder}/ceph.monmap",
                "--keyring",
                f"{self.folder}/{ceph.MON_KEYRING}",
            ]
        )

    def _create_monmap(self) -> None:
        """Run's the ceph tool monmap to create the monmap for the cluster.

        Returns:
            A ceph.monmap file in the folder location.
        """
        subprocess.run(
            [
                "monmaptool",
                "--create",
                "--clobber",
                "--add",
                self.hostname,
                self.ip,
                "--fsid",
                self.fsid,
                f"{self.folder}/ceph.monmap",
            ]
        )

    def _write_config_file(self) -> None:
        """Write the config file for ceph.

        Returns:
            A file in the folder specified as ceph.conf
        """
        config = configparser.ConfigParser()
        config["global"] = {
            "fsid": self.fsid,
            "mon initial members": self.hostname,
            "mon host": self.ip,
            "public network": self.ip_netmask,
            "cluster network": self.ip_netmask,
            "auth cluster required": ceph.AUTH,
            "auth service required": ceph.AUTH,
            "auth client required": ceph.AUTH,
            "osd pool default size": "1",  # Sets replication to 1
            "osd pool default pg autoscale mode": "off",  # Stops autoscaling
            "log flush on exit": "false",  # Stops logging
            "log file": "/dev/null",  # Sets logging to /dev/null
            "mon cluster log": "/dev/null",  # Sets logging to /dev/null
            "mon allow pool delete": "true",  # Allows deletion of pools
        }
        with open(f"{self.folder}/{ceph.CONFIG_FILE}", "w") as configfile:
            config.write(configfile)

    def remove_mon(self) -> None:
        """Remove the Ceph monitor.

        Examples:
            >>> mon.remove_mon()
        """
        system.stop_service("ceph-mon.target")
        system.disable_service("ceph-mon.target")
        system.stop_service("system-ceph\\x2dmon.slice")
        fileio.remove_dir(f"{ceph.VAR_MON}{self.hostname}")


_mon = MON(name="ceph", MON=CephMON)

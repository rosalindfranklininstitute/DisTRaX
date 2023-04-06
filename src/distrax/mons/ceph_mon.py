from distrax.mons.abstract_mon import AbstractMON
import distrax.utils.fileio
import distrax.utils.network as network
import distrax.utils.fileio as fileio
import distrax.utils.system as system
import distrax.utils.ceph as ceph
import uuid
import configparser
import os
import subprocess


class CephMON(AbstractMON):
    """
    Ceph Monitor Class

    This class contains all the methods required to create and remove a Ceph Monitor
    """

    def __init__(self, folder: str = "ceph"):
        """
        Initialise the CephMON object

        Args:
            folder: the place to place the keys of the ceph system

        Examples:
            >>> ceph_mon = CephMON()
        """
        self.auth = "cephx"
        self.config_file = "ceph.conf"
        self.hostname = network.hostname()
        self.fsid = None
        self.ip = None
        self.ip_netmask = None
        self.folder = folder

    def create_mon(self, interface: str):
        """
        Create the Ceph Monitor daemon

        Args:
            interface: the network interface the cluster will be using.
        """

        # Get system details
        self.fsid = uuid.uuid4().hex
        self.ip = network.ip_address_from_network_interface(interface)
        self.ip_netmask = network.ip_with_netmask(self.ip)
        self.hostname = network.hostname()
        # Create required self.folders
        fileio.create_dir(f"{ceph.VAR_MON}{self.hostname}", 0o755)
        fileio.create_dir(self.folder, 0o775)
        # Write config
        self._write_config_file(self.folder)
        fileio.copy_file(
            f"{self.folder}/{self.config_file}", f"{ceph.ETC_CEPH}{self.config_file}"
        )
        # Create keys
        mon_keyring = ceph.create_mon_key(self.folder)
        admin_key = ceph.create_admin_key(self.folder)
        osd_key = ceph.create_osd_key(self.folder)
        distrax.utils.fileio.append_file_in_self.folder(
            self.folder, mon_keyring, [admin_key, osd_key]
        )
        # Create Monmap
        self._create_monmap(self.folder)
        fileio.recursive_change_ownership(self.folder, os.getlogin(), os.getlogin())
        # Create Cluster
        self._create_cluster(mon_keyring, self.folder)
        # Copy files
        fileio.copy_file(
            f"{self.folder}/{mon_keyring}", f"{ceph.VAR_MON}{self.hostname}/keyring"
        )
        fileio.recursive_change_ownership(
            f"{ceph.VAR_MON}{self.hostname}", "ceph", "ceph"
        )
        fileio.copy_file(f"{self.folder}/{admin_key}", f"{ceph.ETC_CEPH}{admin_key}")

        # Start Monitor
        system.start_service(f"ceph-mon@{self.hostname}")
        subprocess.run(["ceph", "mon", "enable-msgr2"])

    def _create_cluster(self, mon_key: str):
        """
        Create the Ceph Cluster with the monitor node
        Args:
            mon_key: The filename of the mon key generated
            self.folder: self.folder where the key is placed
        """

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
                f"{self.folder}/{mon_key}",
            ]
        )

    def _create_monmap(self):
        """
        Run's the ceph tool monmap to create the monmap for the cluster

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

    def _write_config_file(self):
        """
        Write the config file for ceph

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
            "auth cluster required": self.auth,
            "auth service required": self.auth,
            "auth client required": self.auth,
            "osd pool default size": 1,  # Sets replication to 1
            "osd pool default pg autoscale mode": "off",  # Stops autoscaling
            "log flush on exit": "false",  # Stops logging
            "log file": "/dev/null",  # Sets logging to /dev/null
            "mon cluster log": "/dev/null",  # Sets logging to /dev/null
        }
        with open(f"{self.folder}/{self.config_file}", "w") as configfile:
            config.write(configfile)

    def remove_mon(self) -> bool:
        """
        Remove the Ceph monitor

        Returns:
            True if mon is removed, otherwise False

        Examples:
            >>> CephMON().remove_mon()
        """
        system.stop_service("ceph-mon.target")
        system.disable_service("ceph-mon.target")
        system.stop_service("system-ceph\\x2dmon.slice")
        fileio.remove_dir(f"{ceph.VAR_MON}{self.hostname}")

import subprocess
import time

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.network as network
import distrax.utils.system as system
from distrax.exceptions.exceptions import DaemonNotStartedError, MDSNotStartedError
from distrax.mdss import MDS
from distrax.pools.ceph_pool import CephPool


class CephMDS:
    """Ceph Metdata Server Class.

    This class contains all the methods required to create and remove a Ceph Metadata
    Server

    To read more about the Ceph Metadata Server please see:
    https://docs.ceph.com/en/latest/glossary/#term-MDS

    Examples:
        >>> mgr = CephMDS()

        >>> mgr = CephMDS(folder="distrax")
    """

    def __init__(self, folder: str = "ceph", timeout: int = 5):
        """Initialise the CephMDS object.

        Args:
            folder: the location to store the keys of the ceph system

        Examples:
        >>> mds = CephMDS()

        >>> mds = CephMDS(folder="distrax")
        """
        self.hostname = network.hostname()
        self.folder = folder
        self.timeout = timeout

    def create_mds(self) -> None:
        """Create the Ceph MDS Daemon.

        This Daemon operates with the cluster to store all the filesystem
        metadata and allow the filesystem to be created.

        Examples:
            >>> mds.create_mds()
        """
        # Create key
        mds_keyring = self._add_mds()
        # Create MDS directory
        fileio.create_dir(f"{ceph.VAR_MDS}{self.hostname}", 755, admin=True)
        # Copy the key to the folder
        fileio.copy_file(
            f"{self.folder}/{mds_keyring}",
            f"{ceph.VAR_MDS}{self.hostname}/keyring",
            admin=True,
        )
        # Change the ownership of the folder to ceph
        fileio.recursive_change_ownership(
            f"{ceph.VAR_MDS}{self.hostname}", "ceph", "ceph", admin=True
        )
        # Start the Daemon
        system.start_service(f"ceph-mds@{self.hostname}")
        status = system.is_systemd_service_active(f"ceph-mds@{self.hostname}")
        if status is False:
            message = "Ceph MDS Daemon Failed to Start, please investigate"
            raise DaemonNotStartedError(message)
        # Pools required for the MDS
        pool = CephPool()
        pool.create_pool(name="cephfs_data", percentage=0.90)
        pool.create_pool(name="cephfs_metadata", percentage=0.10)
        # Create the filesystem for the MDS
        subprocess.run(
            ["ceph", "fs", "new", "cephfs", "cephfs_metadata", "cephfs_data"]
        )
        # Ensure that the filesystem has joined the cluster.
        mds_started = False
        start = time.time()
        while mds_started is False:
            time.sleep(0.1)
            mds_started = ceph.mds_status()
            if time.time() - start > self.timeout:
                raise MDSNotStartedError("Ceph MDS failed to start")

    def _add_mds(self) -> str:
        """Adds the MDS keys to the ceph system.

        The settings allow the MDS to access
        the Object Storage Devices (osd) and Monitor.

        Returns: the name of the keyring ceph.mds.keyring

        Examples:
            >>>mds._add_mds()
                ceph.mds.keyring
        """
        subprocess.run(
            [
                "ceph",
                "auth",
                "get-or-create",
                f"mds.{self.hostname}",
                "osd",
                "allow rwx",
                "mds",
                "allow",
                "mon",
                "allow profile mds",
                "-o" f"{self.folder}/ceph.mds.keyring",
            ]
        )
        return "ceph.mds.keyring"

    def remove_mds(self) -> None:
        """Remove the Ceph MDS Daemon.

        Examples:
            >>> mds.remove_mds()
        """
        # Stop the filesystem
        subprocess.run(["ceph", "fs", "fail", "cephfs", "--connect-timeout", "5"])
        # Remeove the filesystem
        subprocess.run(
            [
                "ceph",
                "fs",
                "rm",
                "cephfs",
                "--yes-i-really-mean-it",
                "--connect-timeout",
                "5",
            ]
        )
        # Stop the mds
        system.stop_service("ceph-mds.target")
        system.disable_service("ceph-mds.target")
        system.stop_service("system-ceph\\x2dmds.slice")
        fileio.remove_dir(f"{ceph.VAR_MDS}{self.hostname}")


_mds = MDS("ceph", CephMDS)

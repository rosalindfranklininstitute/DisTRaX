import subprocess
import time

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.network as network
import distrax.utils.system as system
from distrax.pools.ceph_pool import CephPool


class CephGateway:
    """Ceph Gateway Class.

    This class contains all the methods required to create and remove a Ceph Gateway

    To read more about the Ceph Gateway please see:
    https://docs.ceph.com/en/latest/glossary/#term-RGW

    Examples:
        >>> gateway = CephGateway()

        >>> gateway = CephGateway(folder="ceph")
    """

    def __init__(self, folder: str = "ceph"):
        """Initialise the CephMGR object.

        Args:
            folder: the location to store the keys of the ceph system

        Examples:
        >>> gateway = CephGateway()

        >>> gateway = CephGateway(folder="ceph")
        """
        self.hostname = network.hostname()
        self.folder = folder

    def create_gateway(self) -> None:
        """Create the Ceph Rados Gateway Daemon.

        This Daemon operates with the monitor to provide additional
        monitoring and interfacing to external tools.

        Examples:
            >>> gateway.create_gateway()
        """
        # Create key
        rgw_keyring = self._add_gateway()
        # Create MGR directory
        fileio.create_dir(f"{ceph.VAR_RGW}{self.hostname}", 0o755)
        # Copy the key to the folder
        fileio.copy_file(
            f"{self.folder}/{rgw_keyring}", f"{ceph.VAR_RGW}{self.hostname}/keyring"
        )
        # Change the ownership of the folder to ceph
        fileio.recursive_change_ownership(
            f"{ceph.VAR_RGW}{self.hostname}", "ceph", "ceph"
        )
        # Pools required for the RadosGateway
        pool = CephPool()
        pool.create_pool(name=".rgw.root", percentage=0.05)
        pool.create_pool(name="default.rgw.control", percentage=0.02)
        pool.create_pool(name="default.rgw.meta", percentage=0.02)
        pool.create_pool(name="default.rgw.log", percentage=0.02)
        pool.create_pool(name="default.rgw.buckets.index", percentage=0.05)
        pool.create_pool(name="default.rgw.buckets.data", percentage=0.84)

        # Start the Daemon
        system.start_service(f"ceph-radosgw@radosgw.{self.hostname}")
        # Ensure that the service has joined the cluster.
        gateway_started = False
        while gateway_started is False:
            time.sleep(0.1)
            gateway_started = ceph.rgw_status()

    def _add_gateway(self) -> str:
        """Adds the manager keys to the ceph system.

        The settings allow the mgr to access
        the Object Storage Devices (osd) and Metadata Sever (MDS) and Monitor.

        Returns: the name of the keyring ceph.mgr.keyring

        Examples:
            >>>gateway._add_gateway()
                ceph.client.radosgw.keyring
        """
        subprocess.run(
            [
                "ceph",
                "auth",
                "get-or-create",
                f"client.radosgw.{self.hostname}",
                "mon",
                "allow *",
                "osd",
                "allow *",
                "-o" f"{self.folder}/ceph.client.radosgw.keyring",
            ]
        )
        return "ceph.client.radosgw.keyring"

    @staticmethod
    def create_s3_user(
        id: str = "admin", access_key: str = "admin", secret_key: str = "admin"
    ) -> None:
        """Create s3 user.

        Args:
            id: id of the user
            access_key: Key for credentials
            secret_key: Secret for credentials

        Examples:
            >>> gateway.create_s3_user(id="admin", access_key="1234", secret_key="abcd")
        """
        subprocess.run(
            ["radosgw-admin", "user", "create", f"--uid={id}", f"--display-name={id}"]
        )
        subprocess.run(
            [
                "radosgw-admin",
                "key",
                "create",
                f"--uid={id}",
                "--key-type=s3",
                f"--secret={secret_key}",
                f"--access-key={access_key}",
            ]
        )

    def remove_gateway(self) -> None:
        """Remove the Ceph RadosGateway Daemon.

        Examples:
            >>> gateway.remove_gateway()
        """
        system.stop_service("ceph-radosgw.target")
        system.disable_service("ceph-radosgw.target")
        system.stop_service("system-ceph\\x2radosgw.slice")
        fileio.remove_dir(f"{ceph.VAR_RGW}{self.hostname}")

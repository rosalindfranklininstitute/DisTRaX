import configparser
import json
import subprocess
import time

from ..utils import ceph as ceph
from ..utils import fileio as fileio
from ..utils import network as network
from ..utils import system as system
from . import GATEWAY
from ..pools.ceph_pool import CephPool


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
        fileio.create_dir(f"{ceph.VAR_RGW}{self.hostname}", 755, admin=True)
        # Copy the key to the folder
        fileio.copy_file(
            f"{self.folder}/{rgw_keyring}",
            f"{ceph.VAR_RGW}{self.hostname}/keyring",
            admin=True,
        )
        # Change the ownership of the folder to ceph
        fileio.recursive_change_ownership(
            f"{ceph.VAR_RGW}{self.hostname}", "ceph", "ceph", admin=True
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

    def create_s3_user(self) -> None:
        """Create s3 user, along with a credentials_file.

        Examples:
            >>> gateway.create_s3_user()

        Returns:
            credentials_file in the form:

            [default]
            user = distrax
            access_key = xxxx
            secret_key = xxxx
            endpoint = http://xxxx:7480:/

        """
        name: str = "distrax"
        user_creation = subprocess.run(
            [
                "radosgw-admin",
                "user",
                "create",
                f"--uid={name}",
                f"--display-name={name}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        user_creation_dict = json.loads(user_creation.stdout.decode())

        with open(f"{self.folder}/credentials", "w") as credentials_file:
            credentials = configparser.ConfigParser()
            config = configparser.ConfigParser()
            config.read(f"{self.folder}/{ceph.CONFIG_FILE}")
            credentials.add_section("default")
            user = user_creation_dict["keys"][0]["user"]
            credentials.set("default", "user", user)
            access_key = user_creation_dict["keys"][0]["access_key"]
            credentials.set("default", "access_key", access_key)
            secret_key = user_creation_dict["keys"][0]["secret_key"]
            credentials.set("default", "secret_key", secret_key)
            credentials.set(
                "default", "endpoint", f"http://{config['global']['mon host']}:7480/"
            )
            credentials.write(credentials_file)

    def remove_gateway(self) -> None:
        """Remove the Ceph RadosGateway Daemon.

        Examples:
            >>> gateway.remove_gateway()
        """
        system.stop_service("ceph-radosgw.target")
        system.disable_service("ceph-radosgw.target")
        system.stop_service("system-ceph\\x2dradosgw.slice")
        fileio.remove_dir(f"{ceph.VAR_RGW}{self.hostname}", admin=True)


_gateway = GATEWAY("ceph", CephGateway)

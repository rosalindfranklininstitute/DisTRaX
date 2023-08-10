import subprocess

import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.network as network
import distrax.utils.system as system
from distrax.exceptions.exceptions import DaemonNotStartedError
from distrax.mgrs import MGR


class CephMGR:
    """Ceph Manager Class.

    This class contains all the methods required to create and remove a Ceph Manager

    To read more about the Ceph Manager please see:
    https://docs.ceph.com/en/latest/glossary/#term-Ceph-Manager

    Examples:
        >>> mgr = CephMGR()

        >>> mgr = CephMGR(folder="distrax")
    """

    def __init__(self, folder: str = "ceph"):
        """Initialise the CephMGR object.

        Args:
            folder: the location to store the keys of the ceph system

        Examples:
        >>> mgr = CephMGR()

        >>> mgr = CephMGR(folder="distrax")
        """
        self.hostname = network.hostname()
        self.folder = folder

    def create_mgr(self) -> None:
        """Create the Ceph Manager Daemon.

        This Daemon operates with the monitor to provide additional
        monitoring and interfacing to external tools.

        Examples:
            >>> mgr.create_mgr()
        """
        # Create key
        mgr_keyring = self._add_mgr()
        # Create MGR directory
        fileio.create_dir(f"{ceph.VAR_MGR}{self.hostname}", 0o755)
        # Copy the key to the folder
        fileio.copy_file(
            f"{self.folder}/{mgr_keyring}", f"{ceph.VAR_MGR}{self.hostname}/keyring"
        )
        # Change the ownership of the folder to ceph
        fileio.recursive_change_ownership(
            f"{ceph.VAR_MGR}{self.hostname}", "ceph", "ceph"
        )
        # Start the Daemon
        system.start_service(f"ceph-mgr@{self.hostname}")
        status = system.is_systemd_service_active(f"ceph-mgr@{self.hostname}")
        if status is False:
            message = "Ceph Manager Failed to Start, please investigate"
            raise DaemonNotStartedError(message)

    def _add_mgr(self) -> str:
        """Adds the manager keys to the ceph system.

        The settings allow the mgr to access
        the Object Storage Devices (osd) and Metadata Sever (MDS) and Monitor.

        Returns: the name of the keyring ceph.mgr.keyring

        Examples:
            >>>mgr._add_mgr()
                ceph.mgr.keyring
        """
        subprocess.run(
            [
                "ceph",
                "auth",
                "get-or-create",
                f"mgr.{self.hostname}",
                "mon",
                "allow profile mgr",
                "osd",
                "allow *",
                "mds",
                "allow *",
                "-o" f"{self.folder}/ceph.mgr.keyring",
            ]
        )
        return "ceph.mgr.keyring"

    def remove_mgr(self) -> None:
        """Remove the Ceph Manager Daemon.

        Examples:
            >>> mgr.remove_mgr()
        """
        system.stop_service("ceph-mgr.target")
        system.disable_service("ceph-mgr.target")
        system.stop_service("system-ceph\\x2dmgr.slice")
        fileio.remove_dir(f"{ceph.VAR_MGR}{self.hostname}")


_mgr = MGR(name="ceph", MGR=CephMGR)

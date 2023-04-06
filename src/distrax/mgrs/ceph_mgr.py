from distrax.mgrs.abstract_mgr import AbstractMGR
import distrax.utils.ceph as ceph
import distrax.utils.fileio as fileio
import distrax.utils.system as system
import distrax.utils.network as network
import subprocess


class CephMGR(AbstractMGR):
    """
    Ceph Manager Class

    This class contains all the methods required to create and remove a Ceph Manager

    Args:
        folder (`str`, optional): The folder to place files created

    Attributes:
        hostname (str): The hostname of the machine
        folder (str): The folder to place files created

    Examples:
        >>> mgr = CephMGR()
    """

    def __init__(self, folder: str = "ceph"):

        self.hostname = network.hostname()
        self.folder = folder

    def create_mgr(self) -> bool:
        """

        Create the Ceph Manager Daemon

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

    def _add_mgr(self) -> str:
        """
        Adds the manager keys to the ceph system, the settings allow the mgr to access
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

    def remove_mgr(self) -> bool:
        """
        Remove the Ceph Manager Daemon

        Examples:
            >>> mgr.remove_mgr()
        """
        system.stop_service("ceph-mgr.target")
        system.disable_service("ceph-mgr.target")
        system.stop_service("system-ceph\\x2dmgr.slice")
        fileio.remove_dir(f"{ceph.VAR_MGR}{self.hostname}")

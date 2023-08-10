import configparser
import json
import os
import subprocess
import time

import distrax.utils.fileio as fileio
from distrax.exceptions.exceptions import MountingFilesystemError
from distrax.filesystems import FILESYSTEM


class CephFilesystem:
    """Ceph Filesystem Class.

    This class contains all the methods required to mount and unmount a Ceph Filesystem

    To read more about the Ceph Gateway please see:
    https://docs.ceph.com/en/latest/glossary/#term-CephFS

    Examples:
        >>> filesystem = CephFilesystem()

        >>> filesystem = CephFilesystem(folder="ceph")
    """

    def __init__(self, folder: str = "ceph", timeout: int = 5):
        """Initialise the CephFilesystem object.

        Examples:
        >>> filesystem = CephFilesystem()
        """
        self.mount_point: str = "/mnt/distrax"
        self.folder = folder
        self.timeout = timeout

    def mount_filesystem(self) -> None:
        """Mount the Ceph Filesystem.

        This mounts the filesystem for the user in the /mnt/distrax/ location

        Examples:
            >>> filesystem.mount_filesystem()
        """
        # Get user
        user = os.getlogin()
        # Get admin key
        admin_key = subprocess.run(
            ["ceph", "auth", "print-key", "client.admin"], stdout=subprocess.PIPE
        ).stdout.decode()
        # Create Filesystem directory
        fileio.create_dir(self.mount_point, 755, admin=True)

        # Mount filesystem
        mounted = False
        start = time.time()
        while mounted is False:
            subprocess.run(
                [
                    "sudo",
                    "mount",
                    "-t",
                    "ceph",
                    ":/",
                    self.mount_point,
                    "-o",
                    f"name=admin,secret={admin_key}",
                ]
            )
            mounted = os.path.ismount(self.mount_point)
            time.sleep(0.1)
            if time.time() - start > self.timeout:
                raise MountingFilesystemError(
                    "Mounting Ceph Filesystem timed out and failed. "
                    "Ensure all the correct packages are "
                    "installed for operating the ceph filesystem, i,e, ceph-mds."
                )

        # Change the ownership of the folder to ceph
        fileio.recursive_change_ownership(self.mount_point, user, user, admin=True)

    def unmount_filesystem(self) -> None:
        """Unmount the Ceph filesystem.

        Examples:
            >>> filesystem.unmount_filesystem()
        """
        # Unmount filesystem
        subprocess.run(["umount", self.mount_point])
        # Remove directory
        fileio.remove_dir(self.mount_point)


_filesystem = FILESYSTEM("ceph", CephFilesystem)

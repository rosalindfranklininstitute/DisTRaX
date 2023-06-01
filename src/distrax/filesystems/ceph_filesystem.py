import os
import subprocess
import time

import distrax.utils.fileio as fileio


class CephFilesystem:
    """Ceph Filesystem Class.

    This class contains all the methods required to mount and unmount a Ceph Filesystem

    To read more about the Ceph Gateway please see:
    https://docs.ceph.com/en/latest/glossary/#term-CephFS

    Examples:
        >>> filesystem = CephFilesystem()

        >>> filesystem = CephFilesystem(folder="ceph", mount_point="cephfs")
    """

    def __init__(self, mount_point: str = "cephfs"):
        """Initialise the CephFilesystem object.

        Args:
            mount_point: The name of the directory in /mnt

        Examples:
        >>> filesystem = CephFilesystem()

        >>> filesystem = CephFilesystem(mount_point="cephfs")
        """
        self.mount_point = "/mnt/" + mount_point

    def mount_filesystem(self) -> None:
        """Mount the Ceph Filesystem.

        This mounts the filesystem for the user in the /mnt location

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
        fileio.create_dir(self.mount_point, 0o755)

        # Mount filesystem
        mounted = False
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
        # Change the ownership of the folder to ceph
        fileio.recursive_change_ownership(self.mount_point, user, user)

    def unmount_filesystem(self) -> None:
        """Unmount the Ceph filesystem.

        Examples:
            >>> filesystem.unmount_filesystem()
        """
        # Unmount filesystem
        subprocess.run(["sudo", "umount", self.mount_point])
        # Remove directory
        fileio.remove_dir(self.mount_point)

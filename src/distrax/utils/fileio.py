import os
import shutil
import subprocess
from typing import List


def create_dir(path: str, mode: int, admin: bool = False) -> bool:
    """Create new directory with the path and mode specified.

    Args:
        path: The path of the folder
        mode: The permissions of the directory using linux access codes
        admin: To run under escalted privileges

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.create_dir("directory_path", 664)
    """
    if os.path.exists(path) is True:
        return False
    command = ""
    if admin:
        command += "sudo "
    command += f"mkdir -p -m {mode} {path}"
    command_lst = command.split()
    process = subprocess.run(
        command_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        return False
    return True


def remove_dir(path: str, admin: bool = False) -> bool:
    """Remove a directory and contents of the path specified.

    Args:
        path: The path to the folder
        admin: To run under escalted privileges

    Returns:
        True if successful else False
    Examples:
        >>> distrax.utils.fileio.remove_dir("folder_exists")
        True
        >>> distrax.utils.fileio.remove_dir("non_existent_folder")
        False
    """
    command = ""
    if admin:
        command += "sudo "
    command += f"find {path} -mindepth 0 -delete"
    command_lst = command.split()
    process = subprocess.run(
        command_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        return False
    return True


def copy_file(src: str, dest: str, admin: bool = False) -> bool:
    """Copy a file from src to dest.

    Maintaining Permissions but no other metadata.

    Args:
        src: path to the file that will be copied
        dest: Destination of the file
        admin: To run under escalted privileges

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.copy_file("file_exists", "./new_file")
        True
        >>> distrax.utils.fileio.copy_file("non_existent_file", "./new_file")
        False
    """
    command = ""
    if admin:
        command += "sudo "
    command += f"cp {src} {dest}"
    command_lst = command.split()
    process = subprocess.run(
        command_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        return False
    return True


def remove_file(path: str, admin: bool = False) -> bool:
    """Remove a file at the path specified.

    Args:
        path: The path to the file that will be removed
        admin: To run under escalted privileges

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.remove_file("file_exists")
        True
        >>> distrax.utils.fileio.remove_file("non_existent_file")
        False
    """
    command = ""
    if admin:
        command += "sudo "
    if os.path.exists(path):
        command += f"find {path} -mindepth 0 -delete"
        command_lst = command.split()
        process = subprocess.run(
            command_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if process.returncode != 0:
            return False
        return True
    else:
        return False


def change_ownership(path: str, user: str, group: str, admin: bool = False) -> bool:
    """Change the ownership of a file or directory.

    Args:
        path: path to file/directory to change
        user: the user to change ownership to
        group: the group to change ownership to
        admin: To run under escalted privileges

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.change_ownership("file",user="user",group="grp")
        True
        >>> distrax.utils.fileio.change_ownership("no_file",user="user",group="grp")
        False
    """
    command = ""
    if admin:
        command += "sudo "
    command += f"chown {user}:{group} {path}"
    command_lst = command.split()
    process = subprocess.run(
        command_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        return False
    return True


def recursive_change_ownership(
    path: str, user: str, group: str, admin: bool = False
) -> bool:
    """Recursively change the ownership of a directory and the files within.

    Args:
        path: path of directory to change ownership of
        user: the user to change ownership to
        group: the group to change ownership to
        admin: To run under escalted privileges

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.recursive_change_ownership("folder", "usr", "grp")
        True
        >>> distrax.utils.fileio.recursive_change_ownership("no_folder","usr", "grp")
        False
    """
    command = ""
    if admin:
        command += "sudo "
    command += f"chown -R {user}:{group} {path}"
    command_lst = command.split()
    process = subprocess.run(
        command_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        return False
    return True


def change_permissions(path: str, mode: int) -> bool:
    """Change a files permission to the mode specified.

    Args:
        path: Path of the file to change
        mode: Octal number of linux permissions i.e. 0o755

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.change_permissions("file", 0o775)
        True
        >>> distrax.utils.fileio.change_permissions("no_file",0o775)
        False
    """
    if os.path.exists(path):
        os.chmod(path, mode)
        return True
    else:
        return False


def recursive_change_permissions(path: str, mode: int) -> bool:
    """Recursively change the permissions of a directory and the files to the mode.

    Args:
        path: Path of the file to change
        mode: Octal number of linux permissions i.e. 0o755

    Returns:
        True if successful else False

    Examples:
        >>> distrax.utils.fileio.recursive_change_permissions("folder", 0o775)
        True
        >>> distrax.utils.fileio.recursive_change_permissions("no_folder",0o775)
        False
    """
    if os.path.isdir(path):
        for dir_path, _, filenames in os.walk(path):
            change_permissions(dir_path, mode)
            for filename in filenames:
                change_permissions(os.path.join(dir_path, filename), mode)
        return True
    else:
        return False


def append_file_in_folder(
    folder: str, file_to_update: str, files_to_append: List[str]
) -> None:
    r"""Append file_to_update with the files in files_to_append.

    Write the contents of the files_to_append into the file_to_update, the files must be
    from the same folder.

    Args:
        folder: Where the files are stored
        file_to_update: File to update
        files_to_append: The files to append

    Examples:
        cat ./file1
            hi
        cat ./file2
            hi

        >>> distrax.utils.fileio.append_file_in_folder(".", "file1", ["file2"])

        cat ./file1

            hi\n
            hi

    """
    with open(f"{folder}/{file_to_update}", "ab") as write_file:
        for file in files_to_append:
            write_file.write(b"\r\n")
            with open(f"{folder}/{file}", "rb") as infile:
                shutil.copyfileobj(infile, write_file)

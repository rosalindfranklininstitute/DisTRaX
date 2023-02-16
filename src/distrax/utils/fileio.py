import os
import shutil


def create_dir(path: str, mode: int) -> bool:
    """
    Create new directory with the path and mode specified
    :param path: The path of the folder
    :param mode: The permissions of the directory
    :return: True if successful else False
    """
    if not os.path.exists(path):
        os.mkdir(path=path, mode=mode)
        return True
    else:
        return False


def remove_dir(path: str) -> bool:
    """
    Remove a directory and contents of the path specified
    :param path: The path of the folder
    :return: True if successful else False
    """
    if os.path.exists(path):
        shutil.rmtree(path)
        return True
    else:
        return False


def copy_file(src: str, dest: str) -> bool:
    """
    Copy a file from src to dest. Maintaining Permissions but no other metadata.
    :param src: path to file to copy
    :param dest: Destination of the file
    :return: True if successful else False
    """
    if os.path.exists(src):
        shutil.copy(src, dest)
        return True
    else:
        return False


def remove_file(path: str) -> bool:
    """
    Remove a file at the path specified
    :param path: The path to the file
    :return: True if successful else False
    """
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        return False


def change_ownership(path: str, user: str, group: str) -> bool:
    """
    Change the ownership of a file or directory
    :param path: path of file/directory to change
    :param user: the user to change ownership to
    :param group: the group to change ownership to
    :return: True if successful else False
    """
    if os.path.exists(path):
        shutil.chown(path, user, group)
        return True
    else:
        return False


def recursive_change_ownership(path: str, user: str, group: str) -> bool:
    """
    Recursively change the ownership of a directory and the files within
    :param path: path of directory to change
    :param user: the user to change ownership to
    :param group: the group to change ownership to
    :return: True if successful else False
    """
    if os.path.isdir(path):
        for dir_path, _, filenames in os.walk(path):
            change_ownership(dir_path, user, group)
            for filename in filenames:
                change_ownership(os.path.join(dir_path, filename), user, group)
        return True
    else:
        return False

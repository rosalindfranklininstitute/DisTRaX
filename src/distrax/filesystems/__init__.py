import logging
from importlib import import_module
from typing import List, NamedTuple, Optional, Union

from . import abstract_filesystem

log = logging.getLogger(__name__)

# Filesystem that can be used
AVAILABLE: List[str] = ["ceph"]
"""Filesystems that are supported and can be used."""


class FILESYSTEM(NamedTuple):
    """Structure for filesystem access."""

    name: str
    FILESYSTEM: type[abstract_filesystem.AbstractFilesystem]


def set_filesystem(filesystem: str) -> None:
    """Sets the Filesystem to use.

    Args:
        filesystem: the filesystem to get, i.e. ceph

    Examples:
        >>> distrax.filesystems as filesystem
        >>> filesystem.set_filesystem()
    """
    filesystem = filesystem.lower()
    global _current
    if filesystem in AVAILABLE:
        module_ = import_module(f"distrax.filesystems.{filesystem}_filesystem")
        if hasattr(module_, "_filesystem"):
            log.debug("Switching manger to `%s`", module_._filesystem.name)
            _current = module_._filesystem
        else:
            raise Exception(f"Module `{filesystem}` is not configured correctly.")
    else:
        raise Exception(
            f"Filesystem `{filesystem}` is not available! Choose from: {AVAILABLE}"
        )


def get_filesystem(name: str = "") -> Optional[FILESYSTEM]:
    """Gets the filesystem as specified by the name.

    Args:
        name: Name of a supported filesystem, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.filesystems as filesystems
        >>> filesystem = filesystems.get_filesystem("ceph")
        >>> filesystem.name
            ceph
        >>> filesystem.FILESYSTEM
            CephFilesystem
    """
    if name != "":
        set_filesystem(name)
    if _current is None:
        set_filesystem(AVAILABLE[0])
    return _current


_current: Union[FILESYSTEM, None] = None

import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_osd

log = logging.getLogger(__name__)
AVAILABLE = ["ceph"]
"""OSDs that are supported and can be used."""


class OSD(NamedTuple):
    """Structure for osd access."""

    name: str
    OSD: type[abstract_osd.AbstractOSD]


def set_osd(osd: str) -> None:
    """Sets the OSD to use.

    Args:
        osd: the osd to get, i.e. ceph

    Examples:
        >>> distrax.osds as osd
        >>> osd.set_osd()
    """
    osd = osd.lower()
    global _current
    if osd in AVAILABLE:
        module_ = import_module(f"distrax.osds.{osd}_osd")
        if hasattr(module_, "_osd"):
            log.debug("Switching manger to `%s`", module_._osd.name)
            _current = module_._osd
        else:
            raise Exception(f"Module `{osd}` is not configured correctly.")
    else:
        raise Exception(
            f"Object Storage Device `{osd}` is not available! Choose from: {AVAILABLE}"
        )


def get_osd(name: str = "") -> Optional[OSD]:
    """Gets the osd as specified by the name.

    Args:
        name: Name of a supported osd, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.osds as osds
        >>> osd = osds.get_osd("ceph")
        >>> osd.name
            ceph
        >>> osd.OSD
            CephOSD
    """
    if name != "":
        set_osd(name)
    if _current is None:
        set_osd(AVAILABLE[0])
    return _current


_current: Union[OSD, None] = None

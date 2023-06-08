import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_mds

log = logging.getLogger(__name__)
AVAILABLE = ["ceph"]
"""MDSs that are supported and can be used."""


class MDS(NamedTuple):
    """Structure for mds access."""

    name: str
    MDS: type[abstract_mds.AbstractMDS]


def set_mds(mds: str) -> None:
    """Sets the MDS to use.

    Args:
        mds: the mds to get, i.e. ceph

    Examples:
        >>> distrax.mdss as mds
        >>> mds.set_mds()
    """
    mds = mds.lower()
    global _current
    if mds in AVAILABLE:
        module_ = import_module(f"distrax.mdss.{mds}_mds")
        if hasattr(module_, "_mds"):
            log.debug("Switching manger to `%s`", module_._mds.name)
            _current = module_._mds
        else:
            raise Exception(f"Module `{mds}` is not configured correctly.")
    else:
        raise Exception(
            f"Metadata Server `{mds}` is not available! Choose from: {AVAILABLE}"
        )


def get_mds(name: str = "") -> Optional[MDS]:
    """Gets the mds as specified by the name.

    Args:
        name: Name of a supported mds, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.mdss as mdss
        >>> mds = mdss.get_mds("ceph")
        >>> mds.name
            ceph
        >>> mds.MDS
            CephMDS
    """
    if name != "":
        set_mds(name)
    if _current is None:
        set_mds(AVAILABLE[0])
    return _current


_current: Union[MDS, None] = None

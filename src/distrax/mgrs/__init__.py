import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_mgr

log = logging.getLogger(__name__)
AVAILABLE = ["ceph"]
"""MGRs that are supported and can be used."""


class MGR(NamedTuple):
    """Structure for mgr access."""

    name: str
    MGR: type[abstract_mgr.AbstractMGR]


def set_mgr(mgr: str) -> None:
    """Sets the MGR to use.

    Args:
        mgr: the mgr to get, i.e. ceph

    Examples:
        >>> distrax.mgrs as mgr
        >>> mgr.set_mgr()
    """
    mgr = mgr.lower()
    global _current
    if mgr in AVAILABLE:
        module_ = import_module(f"distrax.mgrs.{mgr}_mgr")
        if hasattr(module_, "_mgr"):
            log.debug("Switching manger to `%s`", module_._mgr.name)
            _current = module_._mgr
        else:
            raise Exception(f"Module `{mgr}` is not configured correctly.")
    else:
        raise Exception(f"Manager `{mgr}` is not available! Choose from: {AVAILABLE}")


def get_mgr(name: str = "") -> Optional[MGR]:
    """Gets the mgr as specified by the name.

    Args:
        name: Name of a supported mgr, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.mgrs as mgrs
        >>> mgr = mgrs.get_mgr("ceph")
        >>> mgr.name
            ceph
        >>> mgr.MGR
            CephMGR
    """
    if name != "":
        set_mgr(name)
    if _current is None:
        set_mgr(AVAILABLE[0])
    return _current


_current: Union[MGR, None] = None

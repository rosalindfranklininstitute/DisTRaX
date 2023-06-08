import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_mon

log = logging.getLogger(__name__)
AVAILABLE = ["ceph"]
"""MONs that are supported and can be used."""


class MON(NamedTuple):
    """Structure for mon access."""

    name: str
    MON: type[abstract_mon.AbstractMON]


def set_mon(mon: str) -> None:
    """Sets the MON to use.

    Args:
        mon: the mon to get, i.e. ceph

    Examples:
        >>> distrax.mons as mon
        >>> mon.set_mon()
    """
    mon = mon.lower()
    global _current
    if mon in AVAILABLE:
        module_ = import_module(f"distrax.mons.{mon}_mon")
        if hasattr(module_, "_mon"):
            log.debug("Switching monitor to `%s`", module_._mon.name)
            _current = module_._mon
        else:
            raise Exception(f"Module `{mon}` is not configured correctly.")
    else:
        raise Exception(f"Monitor `{mon}` is not available! Choose from: {AVAILABLE}")


def get_mon(name: str = "") -> Optional[MON]:
    """Gets the mon as specified by the name.

    Args:
        name: Name of a supported mon, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.mons as mons
        >>> mon = mons.get_mon("ceph")
        >>> mon.name
            ceph
        >>> mon.MON
            CephMON
    """
    if name != "":
        set_mon(name)
    if _current is None:
        set_mon(AVAILABLE[0])
    return _current


_current: Union[MON, None] = None

import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_pool

log = logging.getLogger(__name__)
AVAILABLE = ["ceph"]
"""Pools that are supported and can be used."""


class POOL(NamedTuple):
    """Structure for pool access."""

    name: str
    POOL: type[abstract_pool.AbstractPool]


def set_pool(pool: str) -> None:
    """Sets the Pool to use.

    Args:
        pool: the pool to get, i.e. ceph

    Examples:
        >>> distrax.pools as pool
        >>> pool.set_pool()
    """
    pool = pool.lower()
    global _current
    if pool in AVAILABLE:
        module_ = import_module(f"distrax.pools.{pool}_pool")
        if hasattr(module_, "_pool"):
            log.debug("Switching pool to `%s`", module_._pool.name)
            _current = module_._pool
        else:
            raise Exception(f"Module `{pool}` is not configured correctly.")
    else:
        raise Exception(f"Pool `{pool}` is not available! Choose from: {AVAILABLE}")


def get_pool(name: str = "") -> Optional[POOL]:
    """Gets the pool as specified by the name.

    Args:
        name: Name of a supported pool, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.pools as pools
        >>> pool = pools.get_pool("ceph")
        >>> pool.name
            ceph
        >>> pool.POOL
            CephPool
    """
    if name != "":
        set_pool(name)
    if _current is None:
        set_pool(AVAILABLE[0])
    return _current


_current: Union[POOL, None] = None

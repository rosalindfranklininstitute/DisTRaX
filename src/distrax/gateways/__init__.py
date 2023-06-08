import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_gateway

log = logging.getLogger(__name__)
AVAILABLE = ["ceph"]
"""Gateways that are supported and can be used."""


class GATEWAY(NamedTuple):
    """Structure for gateway access."""

    name: str
    GATEWAY: type[abstract_gateway.AbstractGateway]


def set_gateway(gateway: str) -> None:
    """Sets the Gateway to use.

    Args:
        gateway: the gateway to get, i.e. ceph

    Examples:
        >>> distrax.gateways as gateway
        >>> gateway.set_gateway()
    """
    gateway = gateway.lower()
    global _current
    if gateway in AVAILABLE:
        module_ = import_module(f"distrax.gateways.{gateway}_gateway")
        if hasattr(module_, "_gateway"):
            log.debug("Switching manger to `%s`", module_._gateway.name)
            _current = module_._gateway
        else:
            raise Exception(f"Module `{gateway}` is not configured correctly.")
    else:
        raise Exception(
            f"Gateway `{gateway}` is not available! Choose from: {AVAILABLE}"
        )


def get_gateway(name: str = "") -> Optional[GATEWAY]:
    """Gets the gateway as specified by the name.

    Args:
        name: Name of a supported gateway, i.e. ceph

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.gateways as gateways
        >>> gateway = gateways.get_gateway("ceph")
        >>> gateway.name
            ceph
        >>> gateway.GATEWAY
            CephGateway
    """
    if name != "":
        set_gateway(name)
    if _current is None:
        set_gateway(AVAILABLE[0])
    return _current


_current: Union[GATEWAY, None] = None

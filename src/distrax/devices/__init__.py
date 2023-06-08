import logging
from importlib import import_module
from typing import NamedTuple, Optional, Union

from . import abstract_device

log = logging.getLogger(__name__)
AVAILABLE = ["brd"]
"""Devices that are supported and can be used."""


class DEVICE(NamedTuple):
    """Structure for device access."""

    name: str
    DEVICE: type[abstract_device.AbstractDevice]


def set_device(device: str) -> None:
    """Sets the DEVICE to use.

    Args:
        device: the device to get, i.e. brd

    Examples:
        >>> distrax.devices as device
        >>> device.set_device()
    """
    device = device.lower()
    global _current
    if device in AVAILABLE:
        module_ = import_module(f"distrax.devices.{device}_device")
        if hasattr(module_, "_device"):
            log.debug("Switching manger to `%s`", module_._device.name)
            _current = module_._device
        else:
            raise Exception(f"Module `{device}` is not configured correctly.")
    else:
        raise Exception(f"Device `{device}` is not available! Choose from: {AVAILABLE}")


def get_device(name: str = "") -> Optional[DEVICE]:
    """Gets the device as specified by the name.

    Args:
        name: Name of a supported device, i.e. brd

    Returns:
        A name tuple with the name of the storage and the class

    Examples:
        >>> distrax.devices as devices
        >>> device = devices.get_device("brd")
        >>> device.name
            brd
        >>> device.DEVICE
            BRDDevice
    """
    if name != "":
        set_device(name)
    if _current is None:
        set_device(AVAILABLE[0])
    return _current


_current: Union[DEVICE, None] = None

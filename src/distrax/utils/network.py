import fcntl
import logging
import socket
import struct

logger = logging.getLogger(__name__)


def ip_address_and_netmask_from_network_interface(
    interface: str,
) -> tuple[str, str, str]:
    """Get the ip address either the inet4 or 6 from the network interface provided.

    Args:
        interface: the network interface i.e. eth0, ib0, etc

    Returns:
        A string format of the ip address as *.*.*.*
        The netmask as a str
        Then the *.*.*.*/*

    Raises:
        OSError
            when the interface does not exist

    Examples:
        >>> distrax.utils.network.ip_address_and_netmask_from_network_interface("lo")
            '127.0.0.1', '32', '127.0.0.1/32'
    """
    SIOCGIFADDR = 0x8915
    SIOCGIFNETMASK = 0x891B
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_version_interface = struct.pack("256s", interface.encode("utf_8"))
    try:
        packed_addr = fcntl.ioctl(sock.fileno(), SIOCGIFADDR, bytes_version_interface)[
            20:24
        ]
        netmask = socket.inet_ntoa(
            fcntl.ioctl(sock.fileno(), SIOCGIFNETMASK, bytes_version_interface)[20:24]
        )
        netmask = str(sum(bin(int(x)).count("1") for x in netmask.split(".")))
    except OSError as error:
        logger.debug(f"Interface `{interface}` does not exists")
        raise (error)
    sock.close()
    ip_address = socket.inet_ntop(socket.AF_INET, packed_addr)
    return ip_address, netmask, f"{ip_address}/{netmask}"


def hostname() -> str:
    """Get the hostname of the system.

    Returns:
        The hostname of the machine

    Examples:
        >>> distrax.utils.network.hostname()
            'example.com'
    """
    return socket.gethostname()

import socket
import fcntl
import struct
import ipaddress


def ip_address_from_network_interface(interface: str) -> str:
    """
    Get the ip address either the inet4 or 6 from the network interface provided.

    Args:
        interface: the network interface i.e. eth0, ib0, etc

    Returns:
        A string format of the ip address as *.*.*.*

    Raises:
        OSError
            when the interface does not exist

    Examples:
        >>> distrax.utils.network.ip_address_from_network_interface("lo")
            '127.0.0.1'
    """
    SIOCGIFADDR = 0x8915
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_version_interface = struct.pack("256s", interface.encode("utf_8"))
    packed_addr = fcntl.ioctl(sock.fileno(), SIOCGIFADDR, bytes_version_interface)[
        20:24
    ]
    sock.close()
    ip_address = socket.inet_ntop(socket.AF_INET, packed_addr)
    return ip_address


def hostname() -> str:
    """
    get the hostname of the system
    Returns:
        The hostname of the machine

    Examples:
        >>> distrax.utils.network.hostname()
            'example.com'
    """
    return socket.gethostname()


def ip_with_netmask(ip_address: str) -> str:
    """
    From the ip address get the netmask.

    Args:
        ip_address: the address to get the netmask added to

    Returns:
        a string of the ip address with the netmask added

    Examples:
        >>> distrax.utils.network.ip_with_netmask("127.0.0.1")
            '127.0.0.1/32'
    """
    return ipaddress.ip_interface(ip_address).exploded

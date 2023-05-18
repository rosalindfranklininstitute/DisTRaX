import pytest

import distrax.utils.network as network


class TestNetwork:
    """
    Tests functions within network
    """

    def test_ip_address_from_network_interface(self):
        interface = "lo"
        assert network.ip_address_from_network_interface(interface) == "127.0.0.1"
        # Check that OSError is raised
        with pytest.raises(OSError):
            network.ip_address_from_network_interface("1234")

    def test_ip_with_netmask(self):
        assert network.ip_with_netmask("127.0.0.1") == "127.0.0.1/32"

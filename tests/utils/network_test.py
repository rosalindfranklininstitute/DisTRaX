import pytest

import distrax.utils.network as network


class TestNetwork:
    """
    Tests functions within network
    """

    def test_ip_address_from_network_interface(self):
        interface = "lo"
        ip, netmask, ip_netmask = network.ip_address_and_netmask_from_network_interface(
            interface
        )
        assert ip == "127.0.0.1"
        assert netmask == "8"
        assert ip_netmask == "127.0.0.1/8"
        # Check that OSError is raised
        with pytest.raises(OSError):
            network.ip_address_and_netmask_from_network_interface("1234")

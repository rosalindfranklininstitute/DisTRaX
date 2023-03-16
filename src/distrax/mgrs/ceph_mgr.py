from distrax.mgrs.abstract_mgr import AbstractMGR
from distrax.utils.network import hostname
import distrax.utils.ceph as ceph


class CephMGR(AbstractMGR):
    """
    Ceph Manager Class

    This class contains all the methods required to create and remove a Ceph Manager
    """

    def __int__(self):
        self.hostname = hostname()

    def create_mgr(self, folder: str) -> bool:
        pass

    def remove_mgr(self, folder: str) -> bool:
        pass

import distrax.osds as osds
from distrax.osds.abstract_osd import AbstractOSD


class TestOSDs:
    """
    Testing that the OSDs created are subclasses and instances of the AbstractOSD
    """

    def test_is_subclass_of_abstract_osd(self):
        for osd in osds.AVAILABLE:
            osds.use_osd(osd)
            object_storage_device = osds.get_osd(osd)
            assert issubclass(object_storage_device.OSD, AbstractOSD)

    def test_instance_of_abstract_osd(self):
        for osd in osds.AVAILABLE:
            osds.use_osd(osd)
            object_storage_device = osds.get_osd(osd)
            assert isinstance(object_storage_device.OSD(), AbstractOSD)

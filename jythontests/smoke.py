import unittest

from core.device.device import Device
from core.device.emulator import Emulator
from core.tns.tns_platform_type import Platform


class TestStringMethods(unittest.TestCase):

    def test_01_smoketest(self):
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()
        pass


    def test_02_smoketest(self):
        assert False, "This test will fail"


if __name__ == '__main__':
    unittest.main()
import socket
import time
import unittest
from datetime import datetime

from nose_parameterized import parameterized

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.tns.tns_platform_type import Platform
from core.utils.csv_utils import CsvUtils


class StartTimeTestCase(unittest.TestCase):
    app_dir = "./testapps/"
    apk_ext = ".apk"
    csv_ext = ".csv"
    device_id = "0a9f9d090d5cdaf2"  # Device.get_id(platform=Platform.ANDROID)
    num_start = 3

    @classmethod
    def setUpClass(cls):
        print "setUpClass"
        Emulator.stop()
        Simulator.stop()
        Device.ensure_available(platform=Platform.ANDROID)

    def setUp(self):
        print "setUp"
        # Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

    def tearDown(self):
        print "tearDown"
        # Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

    @classmethod
    def tearDownClass(cls):
        print "tearDownClass"
        CsvUtils.analyze_data("./tmp-template-hello-world-ng-release.csv")

    @parameterized.expand([
        ("template-hello-world-ng-release", "org.nativescript.templatehelloworldng")
    ])
    def test_start_time(self, apk_name, app_id):
        for x in range(0, self.num_start):
            self.base_test(apk_name, app_id)

    def base_test(self, apk_name, app_id):
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

        apk_file_path = self.app_dir + apk_name + self.apk_ext
        Device.install_app(app_file_path=apk_file_path, device_id=self.device_id)
        Device.clear_log(device_id=self.device_id)

        time.sleep(10)
        Device.turn_on_screen(device_id=self.device_id)

        # TODO(vchimev): Is the device locked?

        time.sleep(10)
        Device.start_app(device_id=self.device_id, app_id=app_id)

        time.sleep(10)
        Device.wait_until_app_is_running(device_id=self.device_id, app_id=app_id, timeout=10)
        start_time = Device.get_start_time(self.device_id, app_id=app_id)

        tmp_csv_file_path = "./tmp-" + apk_name + self.csv_ext
        CsvUtils.write(tmp_csv_file_path, [self.datetime_now(),
                                           self.get_hostname(),
                                           self.device_id,
                                           apk_name,
                                           app_id,
                                           start_time])

        Device.stop_application(device_id=self.device_id, app_id=app_id)
        # PerfUtils.plot_data(csv_file_path=csv_file_path, title="Start Time: " + apk_name)
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

    def get_hostname(self):
        return socket.gethostname()

    def datetime_now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    unittest.main()

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
from core.utils.perf_utils import PerfUtils


class StartTimeTestCase(unittest.TestCase):
    # TODO(vchimev):
    device_id = Device.get_id(platform=Platform.ANDROID)
    app_dir = "./testapps/"
    apk_ext = ".apk"
    csv_ext = ".csv"

    @classmethod
    def setUpClass(cls):
        print "setUpClass"
        Emulator.stop()
        Simulator.stop()
        Device.ensure_available(platform=Platform.ANDROID)

    def setUp(self):
        print "setUp"
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

    def tearDown(self):
        print "tearDown"
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

    @classmethod
    def tearDownClass(cls):
        print "tearDownClass"

    @parameterized.expand([
        ("template-hello-world-ng-webpack-uglify-release", "org.nativescript.TestApp"),
        ("SDK-webpack-uglify-release", "org.nativescript.nativescriptsdkexamplesng"),
        ("QSF-release", "org.nativescript.examples")
    ])
    def test_start_time(self, apk_name, app_id):
        apk_file_path = self.app_dir + apk_name + self.apk_ext
        Device.install_app(app_file_path=apk_file_path, device_id=self.device_id)
        Device.clear_log(device_id=self.device_id)

        # TODO(vchimev):
        time.sleep(5)
        Device.start_app(device_id=self.device_id, app_id=app_id)

        # TODO(vchimev):
        time.sleep(10)
        start_time = Device.get_start_time(self.device_id, app_id=app_id)

        csv_file_path = "./" + apk_name + self.csv_ext
        CsvUtils.write(csv_file_path, [datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                       socket.gethostname(),
                                       self.device_id,
                                       apk_name,
                                       app_id,
                                       start_time])
        Device.stop_application(device_id=self.device_id, app_id=app_id)
        PerfUtils.plot_data(csv_file_path=csv_file_path, title="Start Time: " + apk_name)


if __name__ == '__main__':
    unittest.main()

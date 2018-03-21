import csv
import os
from time import sleep

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.settings.settings import ANDROID_PACKAGE, TYPESCRIPT_PACKAGE, WEBPACK_PACKAGE, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS_PASS, ANDROID_KEYSTORE_ALIAS, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.webpack.helpers.helpers import Helpers


def read_data(device_id):
    assert device_id in Device.get_ids(platform=Platform.ANDROID), "{0} not found!".format(device_id)
    csv_file_path = os.path.join(TEST_RUN_HOME, 'tests', 'perf', 'values.csv')
    csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))
    return [tuple(l) for l in csv_list if l[3].startswith(device_id)]


class PerfTests(BaseClass):
    DEVICE_ID = os.getenv('DEVICE_TOKEN', None)
    DATA = read_data(DEVICE_ID)

    @staticmethod
    def assert_time(expected, actual, tolerance=10, error_message="Startup time is not expected."):
        print "Actual startup: " + actual
        print "Expected startup: " + expected
        x = int(expected)
        y = int(actual)
        if actual >= 0:
            diff = abs(x - y) * 1.00
            assert diff <= x * tolerance * 0.01, error_message + str(actual)

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Npm.cache_clean()
        Emulator.stop()
        Simulator.stop()

    def setUp(self):
        Tns.kill()
        BaseClass.tearDown(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @parameterized.expand(DATA)
    def test_android(self, demo, config, device_name, device_id, first_start, second_start):
        Tns.create_app(self.app_name, attributes={"--template": "https://github.com/" + demo})
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        if "-ng" in demo:
            Tns.update_angular(self.app_name)
        if "-ng" in demo or "-ts" in demo:
            Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=self.app_name)
            Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=self.app_name)
        if "vue" not in demo:
            Npm.install(package=WEBPACK_PACKAGE, option='--save-dev', folder=self.app_name)

        attributes = {"--path": self.app_name,
                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                      "--release": ""}

        if "webpack" in config:
            attr = {"--bundle": "", "--env.uglify": "", "--env.aot": ""}
            attributes.update(attr)

        if "snapshot" in config:
            attr = {"--env.snapshot": ""}
            attributes.update(attr)

        Tns.build_android(attributes=attributes)

        app_id = Tns.get_app_id(self.app_name)
        Adb.clear_logcat(device_id=self.DEVICE_ID)
        Adb.stop_application(device_id=self.DEVICE_ID, app_id=app_id)
        Adb.uninstall(app_id=app_id, device_id=self.DEVICE_ID, assert_success=False)
        assert not Adb.is_application_running(device_id=self.DEVICE_ID, app_id=app_id)

        apk = Helpers.get_apk_path(app_name=self.app_name, config='release')
        Adb.install(apk_file_path=apk, device_id=self.DEVICE_ID)
        Device.turn_on_screen(device_id=self.DEVICE_ID)
        sleep(10)

        # Verify first start
        Adb.clear_logcat(device_id=self.DEVICE_ID)
        Adb.start_app(device_id=self.DEVICE_ID, app_id=app_id)
        sleep(10)
        Device.wait_until_app_is_running(device_id=self.DEVICE_ID, app_id=app_id, timeout=10)
        start_time = Device.get_start_time(self.DEVICE_ID, app_id=app_id)
        message = "{0} first start on {1} is {2} ms.".format(demo, device_name, start_time)
        PerfTests.assert_time(expected=first_start, actual=start_time, tolerance=10, error_message=message)

        # Verify second start
        Adb.stop_application(device_id=self.DEVICE_ID, app_id=app_id)
        assert not Adb.is_application_running(device_id=self.DEVICE_ID, app_id=app_id)
        Adb.clear_logcat(device_id=self.DEVICE_ID)
        sleep(5)
        Adb.start_app(device_id=self.DEVICE_ID, app_id=app_id)
        sleep(10)
        Device.wait_until_app_is_running(device_id=self.DEVICE_ID, app_id=app_id, timeout=10)
        start_time = Device.get_start_time(self.DEVICE_ID, app_id=app_id)
        message = "{0} second start on {1} is {2} ms.".format(demo, device_name, start_time)
        PerfTests.assert_time(expected=second_start, actual=start_time, tolerance=10, error_message=message)

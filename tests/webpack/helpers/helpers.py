import csv
import os

from core.device.device import Device
from core.device.helpers.adb import Adb
from core.osutils.file import File
from core.settings.settings import EMULATOR_ID, EMULATOR_NAME, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts


class Helpers(object):

    @staticmethod
    def get_apk_path(app_name, config):
        return os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, app_name + "-release.apk")

    @staticmethod
    def run_android_via_adb(app_name, config, image):
        Tns.kill()
        Helpers.emulator_cleanup(app_name=app_name)
        Helpers.install_and_run_app(app_name=app_name, config=config)
        Helpers.android_screen_match(app_name=app_name, image=image)

    @staticmethod
    def emulator_cleanup(app_name):
        app_id = Tns.get_app_id(app_name)
        Adb.clear_logcat(device_id=EMULATOR_ID)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=app_id)
        Adb.uninstall(app_id=app_id, device_id=EMULATOR_ID, assert_success=False)
        assert not Adb.is_application_running(device_id=EMULATOR_ID, app_id=app_id)

    @staticmethod
    def install_and_run_app(app_name, config):
        Adb.install(apk_file_path=Helpers.get_apk_path(app_name=app_name, config=config), device_id=EMULATOR_ID)
        Adb.start_app(device_id=EMULATOR_ID, app_id="org.nativescript." + app_name)

    @staticmethod
    def android_screen_match(app_name, image):
        app_id = Tns.get_app_id(app_name)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=image)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=Tns.get_app_id(app_name))
        assert not Adb.is_application_running(device_id=EMULATOR_ID, app_id=app_id)

    @staticmethod
    def ios_screen_match(sim_id, image):
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=sim_id, expected_image=image)

    @staticmethod
    def get_android_size(app_name):
        apk_size = os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, app_name + "-release.apk")
        base_path = os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)

        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        vendor_size = File.get_size(os.path.join(base_path, "vendor.js"))
        app_size = File.get_size(apk_size)

        return bundle_js_size, vendor_size, app_size

    @staticmethod
    def get_ios_size(app_name):
        app_path = os.path.join(app_name, 'platforms', 'ios', 'build', 'device', app_name + '.app')
        ipa_path = os.path.join(app_name, 'platforms', 'ios', 'build', 'device', app_name + '.ipa')

        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        vendor_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        app_size = File.get_size(ipa_path)

        return bundle_js_size, vendor_size, app_size

    @staticmethod
    def assert_size(expected, actual, tolerance=5, error_message="Size is not expected."):
        x = int(expected)
        y = int(actual)
        if actual >= 0:
            diff = abs(x - y) * 1.00
            assert diff <= x * tolerance * 0.01, error_message + str(actual)

    @staticmethod
    def assert_sizes(expected_sizes, actual_sizes, tolerance=1):
        print "Config: " + str(expected_sizes[0])
        print "Actual bundle.js size: " + str(actual_sizes[0])
        print "Actual vendor.js size: " + str(actual_sizes[1])
        print "Actual app size: " + str(actual_sizes[2])
        Helpers.assert_size(expected_sizes[1], actual_sizes[0], tolerance, "Actual bundle.js size:")
        Helpers.assert_size(expected_sizes[2], actual_sizes[1], tolerance, "Actual vendor.js size:")
        Helpers.assert_size(expected_sizes[3], actual_sizes[2], tolerance, "Actual app size:")

    @staticmethod
    def verify_size(app_name, config):
        if "android" in config:
            actual_sizes = Helpers.get_android_size(app_name=app_name)
        if "ios" in config:
            actual_sizes = Helpers.get_ios_size(app_name=app_name)

        csv_file_path = os.path.join(TEST_RUN_HOME, 'tests', 'webpack', 'helpers', 'values.csv')
        csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))
        csv_data = [tuple(l) for l in csv_list]
        for item in csv_data:
            if config == item[0]:
                expected_sizes = item

        Helpers.assert_sizes(actual_sizes=actual_sizes, expected_sizes=expected_sizes)

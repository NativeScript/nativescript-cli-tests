import os

from core.device.device import Device
from core.device.helpers.adb import Adb
from core.settings.settings import EMULATOR_ID, EMULATOR_NAME, SIMULATOR_NAME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts


class Helpers(object):
    @staticmethod
    def get_apk_path(app_name, config):
        if "debug" in config.lower():
            return os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, app_name + "-debug.apk")
        else:
            return os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, app_name + "-release.apk")

    @staticmethod
    def get_ipa_path(app_name):
        return os.path.join(app_name, 'platforms', 'ios', 'build', 'device', app_name + '.ipa')

    @staticmethod
    def get_app_path(app_name):
        return os.path.join(app_name, 'platforms', 'ios', 'build', 'emulator', app_name + '.app')

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

"""
Test for specific needs Android ABI Split.
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.folder import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, EMULATOR_ID, EMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from tests.webpack.helpers.helpers import Helpers
from sys import platform


class AbiSplitTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.ensure_available()
        Folder.cleanup(os.path.join(TEST_RUN_HOME, cls.app_name))
        Tns.create_app_ng(cls.app_name)
        Tns.update_webpack(cls.app_name)
        cls.app_id = Tns.get_app_id(cls.app_name)
        devices = Adb.get_devices(include_emulators=False)
        for device in devices:
            Adb.uninstall(cls.app_id, device, assert_success=False)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @staticmethod
    def assert_apk(apk, device, app_id, image, device_id=EMULATOR_ID, device_name=EMULATOR_NAME):
        Adb.install(apk,
                    device)
        Adb.start_app(device, app_id)
        Helpers.android_screen_match(image=image, timeout=90, device_id=device_id, device_name=device_name, tolerance=1)
        Adb.stop_application(device, app_id)
        Adb.uninstall(app_id, device)

    @staticmethod
    def get_device():
        devices = Adb.get_devices(include_emulators=False)

        for device in devices:
            if "emulator" not in device:
                return device

    def test_100_build_app_with_abi_split_and_snapshot(self):
        """
         Test build with abi split and snapshot. Also check if the apk for emulator is working
         https://github.com/NativeScript/android-runtime/issues/1234
        """

        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_PACKAGE, "--path": self.app_name})
        Adb.clear_logcat(device_id=EMULATOR_ID)
        old_string = "webpackConfig: config,"
        new_string = ""

        if platform == "linux" or platform == "linux2":
            new_string = "webpackConfig: config,\
                        targetArchs: [ \"arm\", \"arm64\", \"ia32\" ],\
                        useLibs: true,\
                        androidNdkPath: \"/tns-official/NDK/android-ndk-r18b-linux/\""
        elif platform == "darwin":
            new_string = "webpackConfig: config,\
                        targetArchs: [ \"arm\", \"arm64\", \"ia32\" ],\
                        useLibs: true,\
                        androidNdkPath: \"/tns-official/NDK/android-ndk-r18b-mac/\""

        target_file = os.path.join(self.app_name, 'webpack.config.js')
        File.replace(target_file, old_string, new_string)
        source_js = os.path.join('data', "issues", 'android-runtime-1234', 'app.gradle')
        target_js = os.path.join(self.app_name, 'App_Resources', 'Android', 'app.gradle')
        File.copy(src=source_js, dest=target_js)
        Tns.build_android(
            attributes={'--path': self.app_name, '--device': EMULATOR_ID, "--env.snapshot": "", "--bundle": "",
                        "--release": "", "--key-store-path": "~/keystore/Telerik.keystore",
                        "--key-store-password": "t3l3r1kad", "--key-store-alias": "Telerik",
                        "--key-store-alias-password": "t3l3r1kad"},
            assert_success=False)

        assert File.exists(
            os.path.join(TEST_RUN_HOME, self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH,
                         "app-arm64-v8a-release.apk"))
        assert File.exists(
            os.path.join(TEST_RUN_HOME, self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH,
                         "app-armeabi-v7a-release.apk"))
        assert File.exists(
            os.path.join(TEST_RUN_HOME, self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH,
                         "app-universal-release.apk"))
        assert File.exists(os.path.join(TEST_RUN_HOME, self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH,
                                        "app-x86-release.apk"))

        self.assert_apk(os.path.join(TEST_RUN_HOME, self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH,
                                     "app-x86-release.apk"),
                        EMULATOR_ID, self.app_id, "abi-split-emulator")

        self.assert_apk(
            os.path.join(TEST_RUN_HOME, self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH,
                         "app-universal-release.apk"),
            EMULATOR_ID, self.app_id, "abi-split-emulator")

    def test_201_run_app_with_abi_split_and_snapshot_on_32_phone(self):
        """
         Test if the apk for arm devices is working
         https://github.com/NativeScript/android-runtime/issues/1234
        """
        phone = self.get_device()

        self.assert_apk(
            os.path.join(TEST_RUN_HOME, "Test_apks",
                         "app-armeabi-v7a-release.apk"),
            phone, self.app_id, "abi-split-32-phone", phone, "ARM-32-Phone")

    def test_202_run_app_with_abi_split_and_snapshot_on_64_phone(self):
        """
         Test if the apk for arm64 devices is working
         https://github.com/NativeScript/android-runtime/issues/1234
        """
        phone = self.get_device()

        self.assert_apk(
            os.path.join(TEST_RUN_HOME, "Test_apks",
                         "app-arm64-v8a-release.apk"),
            phone, self.app_id, "abi-split-64-phone", phone, "ARM-64-Phone")

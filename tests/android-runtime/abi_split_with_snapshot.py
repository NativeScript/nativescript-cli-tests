"""
Test for specific needs of Android runtime.
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.osutils.folder import File
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from core.device.helpers.adb import Adb
from core.settings.settings import ANDROID_PACKAGE, EMULATOR_ID, TEST_RUN_HOME, EMULATOR_NAME
from tests.webpack.helpers.helpers import Helpers


class AbiSplitTests(BaseClass):
    custom_js_file = os.path.join(BaseClass.app_name, "app", "my-custom-class.js")
    tns_folder = os.path.join(BaseClass.app_name, TnsAsserts.PLATFORM_ANDROID_SRC_MAIN_PATH, "java", "com", "tns")
    gen_folder = os.path.join(tns_folder, "gen")
    generated_java_file = os.path.join(tns_folder, "MyJavaClass.java")

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.ensure_available()
        Folder.cleanup('./' + cls.app_name)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_100_build_app_with_abi_split_and_snapshot(self):
        Tns.create_app(self.app_name, attributes={"--ng": ""})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_PACKAGE, "--path": self.app_name})
        Adb.clear_logcat(device_id=EMULATOR_ID)
        old_string = "webpackConfig: config,"
        new_string = "webpackConfig: config,\
            targetArchs: [ \"arm\", \"arm64\", \"ia32\" ],\
            useLibs: true,\
            androidNdkPath: \"/home/ubuntu/ndkr18b/android-ndk-r18b\""
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
            self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH + "/app-arm64-v8a-release.apk")
        assert File.exists(
            self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH + "/app-armeabi-v7a-release.apk")
        assert File.exists(
            self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH + "/app-universal-release.apk")
        assert File.exists(self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH + "/app-x86-release.apk")
        Adb.install(self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH + "/app-x86-release.apk",
                    EMULATOR_ID)
        app_id = Tns.get_app_id(self.app_name)
        Adb.start_app(EMULATOR_ID, app_id);
        Helpers.android_screen_match(image="abi-split-emulator", timeout=90)

    def test_201_run_app_with_abi_split_and_snapshot_on_32_phone(self):
        Tns.create_app(self.app_name, attributes={"--ng": ""})
        devices = Adb.get_devices(include_emulators=False)

        phone = ""
        for device in devices:
            if "emulator" not in device:
                    phone = device

        Adb.install("Test_apks" + "/app-armeabi-v7a-release.apk",
                    phone)
        app_id = Tns.get_app_id(self.app_name)
        Adb.start_app(phone, app_id);
        Helpers.android_screen_match(image="abi-split-32-phone", timeout=90, device_id=phone, device_name="ARM-32-Phone")
        Adb.stop_application(phone, app_id)
        Adb.uninstall(app_id, phone)

    def test_202_run_app_with_abi_split_and_snapshot_on_64_phone(self):
        Tns.create_app(self.app_name, attributes={"--ng": ""})
        devices = Adb.get_devices(include_emulators=False)

        phone = ""
        for device in devices:
            if "emulator" not in device:
                    phone = device
        Adb.install("Test_apks" + "/app-arm64-v8a-release.apk",
                    phone)
        app_id = Tns.get_app_id(self.app_name)
        Adb.start_app(phone, app_id);
        Helpers.android_screen_match(image="abi-split-64-phone",  timeout=90, device_id=phone, device_name="ARM-64-Phone")
        Adb.stop_application(phone, app_id)
        Adb.uninstall(app_id, phone)
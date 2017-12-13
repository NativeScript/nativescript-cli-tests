import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts


class WebPackHelloWorldJS(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()
        Tns.create_app(cls.app_name)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def setUp(self):
        Tns.kill()
        self.emulator_cleanup(app_name=self.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_000_build_without_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name})
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="debug"))
        assert 13000000 < apk_size < 13500000, "Actual apk size is" + apk_size
        self.run_android_via_adb(app_name=self.app_name, config="debug")

    def test_001_build_with_bundle(self):
        output = Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""})
        assert "Webpack compilation complete. Watching for file changes." in output

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="debug"))

        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + bundle_js_size
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + starter_js_size
        assert 1200000 < vendor_js_size < 1310000, "Actual vendor_js_size is " + vendor_js_size
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 12000000 < apk_size < 13000000, "Actual apk_size is " + apk_size

        self.run_android_via_adb(app_name=self.app_name, config="debug")

    def test_002_build_release_with_bundle(self):
        output = Tns.build_android(attributes={"--path": self.app_name,
                                               "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                               "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                               "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                               "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                               "--release": "",
                                               "--bundle": ""})
        assert "Webpack compilation complete. Watching for file changes." in output

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 6500 < bundle_js_size < 7000
        assert 30 < starter_js_size < 50
        assert 1200000 < vendor_js_size < 1310000
        assert 1600 < main_page_xml_size < 2000
        assert 11000000 < apk_size < 11500000

        self.run_android_via_adb(app_name=self.app_name, config="release")

    def test_100_build_release_with_and_bundle_and_uglify(self):
        output = Tns.build_android(attributes={"--path": self.app_name,
                                               "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                               "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                               "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                               "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                               "--release": "",
                                               "--bundle": "",
                                               "--env.uglify": ""})
        assert "Webpack compilation complete. Watching for file changes." in output

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 3500 < bundle_js_size < 3750
        assert 30 < starter_js_size < 50
        assert 665000 < vendor_js_size < 670000
        assert 1600 < main_page_xml_size < 2000
        assert 11000000 < apk_size < 11500000

        self.run_android_via_adb(app_name=self.app_name, config="release")

    def test_110_build_release_with_and_bundle_and_snapshot(self):
        output = Tns.build_android(attributes={"--path": self.app_name,
                                               "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                               "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                               "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                               "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                               "--release": "",
                                               "--bundle": "",
                                               "--env.snapshot": ""})
        assert "Webpack compilation complete. Watching for file changes." in output

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 6500 < bundle_js_size < 7000
        assert 30 < starter_js_size < 50
        assert vendor_js_size == 0
        assert 1600 < main_page_xml_size < 2000
        assert 15500000 < apk_size < 16000000

        self.run_android_via_adb(app_name=self.app_name, config="release")

    def test_120_build_release_with_and_bundle_and_snapshot_and_uglify(self):
        output = Tns.build_android(attributes={"--path": self.app_name,
                                               "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                               "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                               "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                               "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                               "--release": "",
                                               "--bundle": "",
                                               "--env.uglify": "",
                                               "--env.snapshot": ""})
        assert "Webpack compilation complete. Watching for file changes." in output

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 3500 < bundle_js_size < 3750
        assert 30 < starter_js_size < 50
        assert vendor_js_size == 0
        assert 1600 < main_page_xml_size < 2000

        assert 15000000 < apk_size < 15500000

        self.run_android_via_adb(app_name=self.app_name, config="release")

    def test_200_run_with_bundle_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        strings = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        self.screen_match(app_name=self.app_name)

    def test_210_run_with_bundle_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        strings = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        self.screen_match(app_name=self.app_name)

    def test_220_run_with_bundle_snapshot_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        strings = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        self.screen_match(app_name=self.app_name)

    def test_230_run_with_bundle_snapshot_and_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        strings = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        self.screen_match(app_name=self.app_name)

    def test_300_run_bundle_two_times(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        strings = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        self.screen_match(app_name=self.app_name)

        Tns.kill()
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        strings = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        self.screen_match(app_name=self.app_name)

    def test_400_build_with_bundle_without_plugin(self):
        Tns.create_app(self.app_name)
        output = Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""}, assert_success=False)
        assert "Passing --bundle requires a bundling plugin." in output
        assert "No bundling plugin found or the specified bundling plugin is invalid." in output

    def get_apk_path(self, app_name, config):
        if "debug" in config.lower():
            return os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, self.app_name + "-debug.apk")
        else:
            return os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, self.app_name + "-release.apk")

    def run_android_via_adb(self, app_name, config):
        Tns.kill()
        self.emulator_cleanup(app_name=app_name)
        self.install_and_run_app(app_name=app_name, config=config)
        self.screen_match(app_name=app_name)

    def emulator_cleanup(self, app_name):
        app_id = Tns.get_app_id(app_name)
        Adb.clear_logcat(device_id=EMULATOR_ID)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=app_id)
        Adb.uninstall(app_id=app_id, device_id=EMULATOR_ID, assert_success=False)
        assert not Adb.is_application_running(device_id=EMULATOR_ID, app_id=app_id)

    def install_and_run_app(self, app_name, config):
        Adb.install(apk_file_path=self.get_apk_path(app_name=app_name, config=config), device_id=EMULATOR_ID)
        Adb.start_app(device_id=EMULATOR_ID, app_id="org.nativescript." + app_name)

    def screen_match(self, app_name):
        app_id = Tns.get_app_id(app_name)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='hello-world-js')
        Adb.stop_application(device_id=EMULATOR_ID, app_id=Tns.get_app_id(app_name))
        assert not Adb.is_application_running(device_id=EMULATOR_ID, app_id=app_id)

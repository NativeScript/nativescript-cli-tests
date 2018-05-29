import unittest

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, CURRENT_OS, \
    IOS_PACKAGE, ANDROID_PACKAGE, SIMULATOR_NAME, WEBPACK_PACKAGE, TYPESCRIPT_PACKAGE
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.webpack.helpers.helpers import Helpers


class WebPackHelloWorldNG(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-ng'
    image_change = 'hello-world-ng-js-css-xml'

    html_change = ['app/item/items.component.html', '[text]="item.name"', '[text]="item.id"']
    ts_change = ['app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter']
    css_change = ['app/app.css', 'core.light.css', 'core.dark.css']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()
        Tns.create_app_ng(cls.app_name, update_modules=True)
        Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=cls.app_name)
        Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=cls.app_name)
        Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})

        if CURRENT_OS == OSType.OSX:
            Simulator.stop()
            cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
            Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

    def setUp(self):
        Tns.kill()
        Helpers.emulator_cleanup(app_name=self.app_name)
        BaseClass.tearDown(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @staticmethod
    def apply_changes(app_name, log, platform):

        # Change JS, XML and CSS
        ReplaceHelper.replace(app_name, WebPackHelloWorldNG.ts_change, sleep=10)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='Stegen Ter', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, WebPackHelloWorldNG.html_change, sleep=10)
        if platform == Platform.ANDROID:
            strings = ['Successfully transferred items.component.html', 'Successfully synced application']
            Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        ReplaceHelper.replace(app_name, WebPackHelloWorldNG.css_change, sleep=10)
        if platform == Platform.ANDROID:
            strings = ['Successfully transferred app.css', 'Successfully synced application']
            Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=120)

        # Verify application looks correct
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=WebPackHelloWorldNG.image_change, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=WebPackHelloWorldNG.SIMULATOR_ID, image=WebPackHelloWorldNG.image_change,
                                     timeout=120)

    @staticmethod
    def revert_changes(app_name, log, platform):
        # Revert changes
        ReplaceHelper.rollback(app_name, WebPackHelloWorldNG.ts_change, sleep=10)
        ReplaceHelper.rollback(app_name, WebPackHelloWorldNG.html_change, sleep=10)
        ReplaceHelper.rollback(app_name, WebPackHelloWorldNG.css_change, sleep=10)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=60)
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=WebPackHelloWorldNG.image_original, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=WebPackHelloWorldNG.SIMULATOR_ID, image=WebPackHelloWorldNG.image_original,
                                     timeout=120)

    def test_001_android_build_release_with_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="ng-android-bundle")
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_001_ios_build_release_with_bundle(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})
        verification_errors = Helpers.verify_size(app_name=self.app_name, config="ng-ios-bundle")
        self.assertEqual([], verification_errors)

    def test_100_android_build_release_with_bundle_and_uglify(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="ng-android-bundle-uglify")
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_100_ios_build_release_with_bundle_and_uglify(self):
        # Hack due to https://github.com/NativeScript/nativescript-cli/issues/3415
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name})
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_PACKAGE})

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                  "--env.uglify": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="ng-ios-bundle-uglify")
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Windows can't build with snapshot.")
    def test_110_android_build_release_with_bundle_and_snapshot(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.snapshot": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="ng-android-bundle-snapshot",
                                                  check_embedded_script_size=True)
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Windows can't build with snapshot.")
    def test_120_android_build_release_with_bundle_and_snapshot_and_uglify(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": "",
                                      "--env.snapshot": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="ng-android-bundle-uglify-snapshot",
                                                  check_embedded_script_size=True)
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    def test_200_run_android_with_bundle_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=self.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_200_run_ios_with_bundle_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.IOS)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.IOS)

    def test_210_run_android_with_bundle_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=self.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_210_run_ios_with_bundle_uglify_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.uglify': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.IOS)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.IOS)

import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, CURRENT_OS, \
    IOS_RUNTIME_PATH, SIMULATOR_NAME, ANDROID_RUNTIME_PATH
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts
from tests.webpack.helpers.helpers import Helpers


class WebPackHelloWorldNG(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-ng'
    image_change = 'hello-world-ng-js-css-xml'

    wp_run = ['Webpack compilation complete', 'Successfully installed']
    wp_errors = ['ERROR', 'Module not found']

    html_change = ['app/item/items.component.html', '[text]="item.name"', '[text]="item.id"']
    ts_change = ['app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter']
    css_change = ['app/app.css', 'core.light.css', 'core.dark.css']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Tns.create_app_ng(cls.app_name, update_modules=True)
        Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=cls.app_name)
        Npm.install(package="nativescript-dev-typescript@next", option='--save-dev', folder=cls.app_name)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

    def setUp(self):
        Tns.kill()
        Helpers.emulator_cleanup(app_name=self.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_000_build_without_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name})
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="debug"))
        assert 26000000 < apk_size < 27000000, "Actual apk size is " + str(apk_size)
        Helpers.run_android_via_adb(app_name=self.app_name, config="debug", image=self.image_original)

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name})

            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})
            app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
            ipa_path = app_path.replace(".app", ".ipa")
            ipa_size = File.get_size(ipa_path)
            assert 26000000 < ipa_size < 27000000, "Actual app is " + str(ipa_size)

    def test_001_android_build_with_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="debug"))

        assert 1300000 < bundle_js_size < 1350000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 3400000 < vendor_js_size < 3500000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 13500000 < apk_size < 14000000, "Actual apk_size is " + str(apk_size)

        Helpers.run_android_via_adb(app_name=self.app_name, config="debug", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_001_ios_build_with_bundle(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--bundle": ""})

        app_path = Helpers.get_app_path(app_name=self.app_name)
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        assert 1300000 < bundle_js_size < 1350000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 3500000 < vendor_js_size < 3600000, "Actual vendor_js_size is " + str(vendor_js_size)

    def test_002_android_build_release_with_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 1300000 < bundle_js_size < 1350000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 3400000 < vendor_js_size < 3500000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 11500000 < apk_size < 12000000, "Actual apk_size is " + str(apk_size)

        Helpers.run_android_via_adb(app_name=self.app_name, config="release", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_002_ios_build_release_with_bundle(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})
        app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
        ipa_path = app_path.replace(".app", ".ipa")
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        ipa_size = File.get_size(ipa_path)
        assert 1300000 < bundle_js_size < 1350000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 3500000 < vendor_js_size < 3600000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 13000000 < ipa_size < 13500000, "Actual app is " + str(ipa_size)

    def test_100_android_build_release_with_and_bundle_and_uglify(self):
        # Workaround for https://github.com/NativeScript/nativescript-dev-webpack/issues/370
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name})
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 450000 < bundle_js_size < 500000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 1300000 < vendor_js_size < 1350000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 11500000 < apk_size < 12000000, "Actual app is " + str(apk_size)

        Helpers.run_android_via_adb(app_name=self.app_name, config="release", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_100_ios_build_release_with_and_bundle_and_uglify(self):
        # Workaround for https://github.com/NativeScript/nativescript-dev-webpack/issues/370
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name})
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                  "--env.uglify": ""})
        app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
        ipa_path = app_path.replace(".app", ".ipa")
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        ipa_size = File.get_size(ipa_path)
        assert 400000 < bundle_js_size < 500000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 685000 < vendor_js_size < 695000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 12500000 < ipa_size < 13000000, "Actual app is " + str(ipa_size)

    def test_110_android_build_release_with_and_bundle_and_snapshot(self):
        # Workaround for https://github.com/NativeScript/nativescript-dev-webpack/issues/370
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name})
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.snapshot": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 1300000 < bundle_js_size < 1350000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert vendor_js_size == 0, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 16000000 < apk_size < 16500000, "Actual app is " + str(apk_size)

        Helpers.run_android_via_adb(app_name=self.app_name, config="release", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_110_ios_build_release_with_and_bundle_and_snapshot(self):
        # Workaround for https://github.com/NativeScript/nativescript-dev-webpack/issues/370
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name})
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                  "--env.snapshot": ""})
        app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
        ipa_path = app_path.replace(".app", ".ipa")
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        ipa_size = File.get_size(ipa_path)
        assert 1300000 < bundle_js_size < 1350000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 3500000 < vendor_js_size < 3600000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 13000000 < ipa_size < 13500000, "Actual app is " + str(ipa_size)

    def test_120_android_build_release_with_and_bundle_and_snapshot_and_uglify(self):
        # Workaround for https://github.com/NativeScript/nativescript-dev-webpack/issues/370
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name})
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": "",
                                      "--env.snapshot": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 450000 < bundle_js_size < 500000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert vendor_js_size == 0, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 14000000 < apk_size < 15000000, "Actual app is " + str(apk_size)

        Helpers.run_android_via_adb(app_name=self.app_name, config="release", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_120_ios_build_release_with_and_bundle_and_snapshot_and_uglify(self):
        # Workaround for https://github.com/NativeScript/nativescript-dev-webpack/issues/370
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name})
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                  "--env.snapshot": "", "--env.uglify": ""})
        app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
        ipa_path = app_path.replace(".app", ".ipa")
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        ipa_size = File.get_size(ipa_path)
        assert 400000 < bundle_js_size < 500000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 680000 < vendor_js_size < 700000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 12500000 < ipa_size < 13000000, "Actual app is " + str(ipa_size)

    def test_200_run_android_with_bundle_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_200_run_ios_with_bundle_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

    def test_210_run_android_with_bundle_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_210_run_ios_with_bundle_uglify_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.uglify': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.uglify': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.uglify': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

    def test_220_run_android_with_bundle_snapshot_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_220_run_ios_with_bundle_snapshot_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

    def test_230_run_android_with_bundle_snapshot_and_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_230_run_ios_with_bundle_snapshot_and_uglify_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': '',
                                      '--env.uglify': ''}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.ts_change)
        ReplaceHelper.replace(self.app_name, self.html_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': '',
                                      '--env.uglify': ''}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.ts_change)
        ReplaceHelper.rollback(self.app_name, self.html_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': '',
                                      '--env.uglify': ''}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

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


class WebPackHelloWorldJS(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-js'
    image_change = 'hello-world-js-js-css-xml'

    wp_run = ['Webpack compilation complete', 'Successfully installed']
    wp_errors = ['ERROR', 'Module not found', 'Error']

    xml_change = ['app/main-page.xml', 'TAP', 'TEST']
    js_change = ['app/main-view-model.js', 'taps', 'clicks']
    css_change = ['app/app.css', '18', '32']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name, update_modules=True)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        if CURRENT_OS == OSType.OSX:
            Simulator.stop()
            cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
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
        assert 13000000 < apk_size < 13500000, "Actual apk size is " + str(apk_size)
        Helpers.run_android_via_adb(app_name=self.app_name, config="debug", image=self.image_original)

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name})

            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})
            app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
            ipa_path = app_path.replace(".app", ".ipa")
            ipa_size = File.get_size(ipa_path)
            assert 13000000 < ipa_size < 13500000, "Actual app is " + str(ipa_size)

    def test_001_android_build_with_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="debug"))

        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 1200000 < vendor_js_size < 1310000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 12000000 < apk_size < 13000000, "Actual apk_size is " + str(apk_size)

        Helpers.run_android_via_adb(app_name=self.app_name, config="debug", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_001_ios_build_with_bundle(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--bundle": ""})

        app_path = Helpers.get_app_path(app_name=self.app_name)
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))
        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 1400000 < vendor_js_size < 1450000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size

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
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 6500 < bundle_js_size < 7000
        assert 30 < starter_js_size < 50
        assert 1200000 < vendor_js_size < 1310000
        assert 1600 < main_page_xml_size < 2000
        assert 11000000 < apk_size < 11500000

        Helpers.run_android_via_adb(app_name=self.app_name, config="release", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_002_ios_build_release_with_bundle(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})
        app_path = Helpers.get_app_path(app_name=self.app_name).replace("emulator", "device")
        ipa_path = app_path.replace(".app", ".ipa")
        bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
        starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
        vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))
        ipa_size = File.get_size(ipa_path)
        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 1400000 < vendor_js_size < 1450000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 12500000 < ipa_size < 13000000, "Actual app is " + str(ipa_size)

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
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 3500 < bundle_js_size < 3750, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 670000 < vendor_js_size < 680000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 11000000 < apk_size < 11500000, "Actual app is " + str(apk_size)

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
        main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))
        ipa_size = File.get_size(ipa_path)
        assert 3500 < bundle_js_size < 3750, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 685000 < vendor_js_size < 695000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
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
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert vendor_js_size == 0, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 13000000 < apk_size < 14000000, "Actual app is " + str(apk_size)

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
        main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))
        ipa_size = File.get_size(ipa_path)
        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 1400000 < vendor_js_size < 1450000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000
        assert 12500000 < ipa_size < 13000000, "Actual app is " + str(ipa_size)

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
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(Helpers.get_apk_path(app_name=self.app_name, config="release"))

        assert 3500 < bundle_js_size < 3750
        assert 30 < starter_js_size < 50
        assert vendor_js_size == 0
        assert 1600 < main_page_xml_size < 2000

        assert 12500000 < apk_size < 13500000, "Actual app is " + str(apk_size)

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
        main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))
        ipa_size = File.get_size(ipa_path)
        assert 3500 < bundle_js_size < 3750
        assert 30 < starter_js_size < 50
        assert 680000 < vendor_js_size < 700000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000
        assert 12500000 < ipa_size < 13000000, "Actual app is " + str(ipa_size)

    def test_200_run_android_with_bundle_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_original)
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.android_screen_match(app_name=self.app_name, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
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
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.uglify': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
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
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': ''},
                          wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
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
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
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
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': '',
                                      '--env.uglify': ''}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--bundle': '', '--env.snapshot': '',
                                      '--env.uglify': ''}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)
        Tns.kill()

    def test_400_build_with_bundle_without_plugin(self):
        Tns.create_app(self.app_name)
        output = Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""}, assert_success=False)
        assert "Passing --bundle requires a bundling plugin." in output
        assert "No bundling plugin found or the specified bundling plugin is invalid." in output

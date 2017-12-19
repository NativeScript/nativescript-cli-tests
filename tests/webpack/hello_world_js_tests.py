import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME, CURRENT_OS, \
    IOS_RUNTIME_PATH, SIMULATOR_NAME, ANDROID_RUNTIME_PATH
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts


class WebPackHelloWorldJS(BaseClass):
    SIMULATOR_ID = ""
    # wp_run = ['Webpack compilation complete', 'Watching for file changes', 'Successfully installed', EMULATOR_ID]
    wp_run = ['Successfully installed', EMULATOR_ID]
    wp_errors = ['ERROR', 'Module not found', 'Error']

    js_template_xml_change = ['app/main-page.xml', 'TAP', 'TEST']
    js_template_js_change = ['app/main-view-model.js', 'taps', 'clicks']
    js_template_css_change = ['app/app.css', '18', '32']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Tns.create_app(cls.app_name, update_modules=True)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

    def setUp(self):
        Tns.kill()
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name})
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})
        if CURRENT_OS is OSType.OSX:
            Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name})
            Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})
        self.emulator_cleanup(app_name=self.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_000_build_without_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name})
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="debug"))
        assert 13000000 < apk_size < 13500000, "Actual apk size is" + str(apk_size)
        self.run_android_via_adb(app_name=self.app_name, config="debug")

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name})

            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})
            app_path = self.get_app_path(app_name=self.app_name).replace("emulator", "device")
            ipa_path = app_path.replace(".app", ".ipa")
            ipa_size = File.get_size(ipa_path)
            assert 13000000 < ipa_size < 13500000, "Actual app is " + str(ipa_size)

    def test_001_build_with_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""})

        base_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        bundle_js_size = File.get_size(os.path.join(base_path, "bundle.js"))
        starter_js_size = File.get_size(os.path.join(base_path, "starter.js"))
        vendor_js_size = File.get_size(os.path.join(base_path, "vendor.js"))
        main_page_xml_size = File.get_size(os.path.join(base_path, "main-page.xml"))
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="debug"))

        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 1200000 < vendor_js_size < 1310000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 12000000 < apk_size < 13000000, "Actual apk_size is " + str(apk_size)

        self.run_android_via_adb(app_name=self.app_name, config="debug")

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name, "--bundle": ""})

            # Simulator build
            app_path = self.get_app_path(app_name=self.app_name)

            bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
            starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
            vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
            main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))

            assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
            assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
            assert 1400000 < vendor_js_size < 1450000, "Actual vendor_js_size is " + str(vendor_js_size)
            assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size

    def test_002_build_release_with_bundle(self):
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
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 6500 < bundle_js_size < 7000
        assert 30 < starter_js_size < 50
        assert 1200000 < vendor_js_size < 1310000
        assert 1600 < main_page_xml_size < 2000
        assert 11000000 < apk_size < 11500000

        self.run_android_via_adb(app_name=self.app_name, config="release")

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})

            app_path = self.get_app_path(app_name=self.app_name).replace("emulator", "device")
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

    def test_100_build_release_with_and_bundle_and_uglify(self):
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
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 3500 < bundle_js_size < 3750, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert 670000 < vendor_js_size < 680000, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 11000000 < apk_size < 11500000, "Actual app is " + str(apk_size)

        self.run_android_via_adb(app_name=self.app_name, config="release")

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                      "--env.uglify": ""})

            app_path = self.get_app_path(app_name=self.app_name).replace("emulator", "device")
            ipa_path = app_path.replace(".app", ".ipa")

            bundle_js_size = File.get_size(os.path.join(app_path, "app", "bundle.js"))
            starter_js_size = File.get_size(os.path.join(app_path, "app", "starter.js"))
            vendor_js_size = File.get_size(os.path.join(app_path, "app", "vendor.js"))
            main_page_xml_size = File.get_size(os.path.join(app_path, "app", "main-page.xml"))
            ipa_size = File.get_size(ipa_path)

            assert 3500 < bundle_js_size < 3750, "Actual bundle_js_size is " + str(bundle_js_size)
            assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
            assert 670000 < vendor_js_size < 680000, "Actual vendor_js_size is " + str(vendor_js_size)
            assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
            assert 12000000 < ipa_size < 12500000, "Actual app is " + str(ipa_size)

    def test_110_build_release_with_and_bundle_and_snapshot(self):
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
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 6500 < bundle_js_size < 7000, "Actual bundle_js_size is " + str(bundle_js_size)
        assert 30 < starter_js_size < 50, "Actual starter_js_size is " + str(starter_js_size)
        assert vendor_js_size == 0, "Actual vendor_js_size is " + str(vendor_js_size)
        assert 1600 < main_page_xml_size < 2000, "Actual main_page_xml_size is " + main_page_xml_size
        assert 13000000 < apk_size < 14000000, "Actual app is " + str(apk_size)

        self.run_android_via_adb(app_name=self.app_name, config="release")

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                      "--env.snapshot": ""})

            app_path = self.get_app_path(app_name=self.app_name).replace("emulator", "device")
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
            assert 12000000 < ipa_size < 12500000, "Actual app is " + str(ipa_size)

    def test_120_build_release_with_and_bundle_and_snapshot_and_uglify(self):
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
        apk_size = File.get_size(self.get_apk_path(app_name=self.app_name, config="release"))

        assert 3500 < bundle_js_size < 3750
        assert 30 < starter_js_size < 50
        assert vendor_js_size == 0
        assert 1600 < main_page_xml_size < 2000

        assert 12500000 < apk_size < 13500000, "Actual app is " + str(apk_size)

        self.run_android_via_adb(app_name=self.app_name, config="release")

        if CURRENT_OS is OSType.OSX:
            Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                      "--env.snapshot": "", "--env.uglify": ""})

            app_path = self.get_app_path(app_name=self.app_name).replace("emulator", "device")
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
            assert 12000000 < ipa_size < 12500000, "Actual app is " + str(ipa_size)

    def test_200_run_with_bundle_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_template_js_change)
        ReplaceHelper.replace(self.app_name, self.js_template_xml_change)
        ReplaceHelper.replace(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        self.screen_match(app_name=self.app_name, image='hello-world-js-js-css-xml')
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_template_js_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_xml_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

    def test_210_run_with_bundle_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_template_js_change)
        ReplaceHelper.replace(self.app_name, self.js_template_xml_change)
        ReplaceHelper.replace(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        self.screen_match(app_name=self.app_name, image='hello-world-js-js-css-xml')
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_template_js_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_xml_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

    def test_220_run_with_bundle_snapshot_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_template_js_change)
        ReplaceHelper.replace(self.app_name, self.js_template_xml_change)
        ReplaceHelper.replace(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        self.screen_match(app_name=self.app_name, image='hello-world-js-js-css-xml')
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_template_js_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_xml_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

    def test_230_run_with_bundle_snapshot_and_uglify_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_template_js_change)
        ReplaceHelper.replace(self.app_name, self.js_template_xml_change)
        ReplaceHelper.replace(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=60)
        self.screen_match(app_name=self.app_name, image='hello-world-js-js-css-xml')
        Tns.kill()

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_template_js_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_xml_change)
        ReplaceHelper.rollback(self.app_name, self.js_template_css_change)

        # Verify application looks correct
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          "--bundle": "",
                                          "--env.snapshot": "",
                                          "--env.uglify": "",
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=self.wp_run, not_existing_string_list=self.wp_errors, timeout=180)
        self.screen_match(app_name=self.app_name, image='hello-world-js')
        Tns.kill()

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

    def get_ipa_path(self, app_name):
        return os.path.join(app_name, 'platforms', 'ios', 'build', 'device', app_name + '.ipa')

    def get_app_path(self, app_name):
        return os.path.join(app_name, 'platforms', 'ios', 'build', 'emulator', app_name + '.app')

    def run_android_via_adb(self, app_name, config):
        Tns.kill()
        self.emulator_cleanup(app_name=app_name)
        self.install_and_run_app(app_name=app_name, config=config)
        self.screen_match(app_name=app_name, image='hello-world-js')

    def emulator_cleanup(self, app_name):
        app_id = Tns.get_app_id(app_name)
        Adb.clear_logcat(device_id=EMULATOR_ID)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=app_id)
        Adb.uninstall(app_id=app_id, device_id=EMULATOR_ID, assert_success=False)
        assert not Adb.is_application_running(device_id=EMULATOR_ID, app_id=app_id)

    def install_and_run_app(self, app_name, config):
        Adb.install(apk_file_path=self.get_apk_path(app_name=app_name, config=config), device_id=EMULATOR_ID)
        Adb.start_app(device_id=EMULATOR_ID, app_id="org.nativescript." + app_name)

    def screen_match(self, app_name, image):
        app_id = Tns.get_app_id(app_name)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=image)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=Tns.get_app_id(app_name))
        assert not Adb.is_application_running(device_id=EMULATOR_ID, app_id=app_id)

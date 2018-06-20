import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS, SIMULATOR_NAME, \
    ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, \
    ANDROID_PACKAGE, IOS_PACKAGE, EMULATOR_ID
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from tests.webpack.helpers.helpers import Helpers


class VueTests(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-vue'
    image_change = 'hello-world-vue-sync'

    js_change = ['app/main.js', 'new', 'Vue.config.silent = false;' + os.linesep + 'new']
    xml_change = ['app/components/Counter.js', '42', '32']
    css_change = ['app/app.css', 'light', 'dark']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name,
                       attributes={"--template": "https://github.com/nativescript-vue/nativescript-vue-template"})
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
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_android_build_release(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": ""})

        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_001_ios_build_release(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})

    def test_200_run_android_and_sync_changes(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=self.image_original)

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.android_screen_match(image=self.image_change)

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.android_screen_match(image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_200_run_ios_and_sync_changes(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_change)
        ReplaceHelper.replace(self.app_name, self.xml_change)
        ReplaceHelper.replace(self.app_name, self.css_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=90, check_interval=5)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_change)

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change)
        ReplaceHelper.rollback(self.app_name, self.xml_change)
        ReplaceHelper.rollback(self.app_name, self.css_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=90, check_interval=5)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=self.image_original)

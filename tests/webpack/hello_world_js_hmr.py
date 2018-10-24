import unittest

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, CURRENT_OS, \
    IOS_PACKAGE, SIMULATOR_NAME, ANDROID_PACKAGE, WEBPACK_PACKAGE
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.webpack.helpers.helpers import Helpers
# import hashlib
# import re


class RunTestsHMR(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-js'
    image_change = 'hello-world-js-js-css-xml'

    xml_change = ['app/main-page.xml', 'TAP', 'TEST']
    js_change = ['app/main-view-model.js', 'taps', 'clicks']
    css_change = ['app/app.css', '18', '32']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name, update_modules=True)
        Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})

        if CURRENT_OS == OSType.OSX:
            Simulator.stop()
            cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
            Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

    def setUp(self):
        Tns.kill()
        Helpers.emulator_cleanup(app_name=self.app_name)
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @staticmethod
    def apply_changes(app_name, log, platform):

        not_found_list = []
        # Change JS, XML and CSS
        ReplaceHelper.replace(app_name, RunTestsHMR.js_change, sleep=10)
        strings = ['JS: HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
                   'Successfully transferred bundle.',
                   'JS: HMR: Successfully applied update with hmr hash ']
        # strings = ['JS: HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
        #            'Successfully transferred bundle.{0}.hot-update.js'.format(hash()),
        #            'JS: HMR: Successfully applied update with hmr hash {0}'.format(hashlib.sha1)]
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, RunTestsHMR.xml_change, sleep=10)
        strings = ['Refreshing application on device', 'JS: HMR: Checking for updates to the bundle with hmr hash',
                   './main-page.xml', 'JS: HMR: Successfully applied update with hmr hash']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, RunTestsHMR.css_change, sleep=10)
        if platform == Platform.ANDROID:
            Tns.wait_for_log(log_file=log, string_list=['app.css'], clean_log=False)

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=120)

        # Verify application looks correct
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=RunTestsHMR.image_change, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=RunTestsHMR.SIMULATOR_ID, image=RunTestsHMR.image_change,
                                     timeout=120)

    @staticmethod
    def apply_changes_js(app_name, log, platform):
        # Change JS
        ReplaceHelper.replace(app_name, RunTestsHMR.js_change, sleep=10)
        strings = ['JS: HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
                   'Successfully transferred bundle.',
                   'JS: HMR: Successfully applied update with hmr hash ']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

    @staticmethod
    def apply_changes_xml(app_name, log, platform):
        # Change XML after uninstall app from device
        ReplaceHelper.replace(app_name, RunTestsHMR.xml_change, sleep=10)
        strings = ['Refreshing application on device',
                   'JS: HMR: Sync...','JS: HMR: Hot Module Replacement Enabled. Waiting for signal.']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

    @staticmethod
    def revert_changes(app_name, log, platform):
        # Clean old logs
        if CURRENT_OS is not OSType.WINDOWS:
            File.write(file_path=log, text="")

        # Revert XML changes
        ReplaceHelper.rollback(app_name, RunTestsHMR.xml_change, sleep=10)
        strings = ['JS: HMR: Sync...', 'Refreshing application on device', './main-page.xml',
                   'JS: HMR: Checking for updates to the bundle with hmr hash']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TAP')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Revert JS changes
        ReplaceHelper.rollback(app_name, RunTestsHMR.js_change, sleep=10)
        strings = ['JS: HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
                   'Successfully transferred bundle.', 'JS: HMR: Successfully applied update with hmr hash ']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left', timeout=20)
            assert text_changed, 'JS: HMR: The following modules were updated:'

        # Revert CSS changes
        ReplaceHelper.rollback(app_name, RunTestsHMR.css_change, sleep=10)
        Tns.wait_for_log(log_file=log, string_list=['app.css'], clean_log=False)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=60)
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=RunTestsHMR.image_original, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=RunTestsHMR.SIMULATOR_ID, image=RunTestsHMR.image_original,
                                     timeout=120)

    def test_001_android_run_hmr(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run_hmr, not_existing_string_list=Helpers.wp_errors_hmr,
                         timeout=240)
        Helpers.android_screen_match(image=self.image_original, timeout=120)

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)

    def test_002_ios_run_hmr(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run_hmr, not_existing_string_list=Helpers.wp_errors_hmr,
                         timeout=240)
        Helpers.ios_screen_match(image=self.image_original, timeout=120)

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.IOS)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.IOS)

    def test_003_android_run_hmr_uninstall_app(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run_hmr, not_existing_string_list=Helpers.wp_errors_hmr,
                         timeout=240)
        Helpers.android_screen_match(image=self.image_original, timeout=120)

        self.apply_changes_js(app_name=self.app_name, log=log, platform=Platform.ANDROID)

        # Uninstall app while `tns run` is running
        Device.uninstall_app(app_prefix='org.nativescript.', platform=Platform.ANDROID)

        self.apply_changes_xml(app_name=self.app_name, log=log, platform=Platform.ANDROID)

        # Verify application looks correct
        if Platform == Platform.ANDROID:
            Helpers.android_screen_match(image=RunTestsHMR.image_change, timeout=120)

    def test_004_ios_run_hmr_uninstall_app(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                            assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run_hmr, not_existing_string_list=Helpers.wp_errors_hmr,
                         timeout=240)
        Helpers.ios_screen_match(image=self.image_original, timeout=120)

        self.apply_changes_js(app_name=self.app_name, log=log, platform=Platform.IOS)

        # Uninstall app while `tns run` is running
        Device.uninstall_app(app_prefix='org.nativescript.', platform=Platform.IOS)

        self.apply_changes_xml(app_name=self.app_name, log=log, platform=Platform.IOS)

    def test_005_android_run_hmr_console_log(self):
        source_js = os.path.join('data', "issues", 'console-log-hmr', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                                      assert_success=False)
        strings = ['JS: LOG']
        Tns.wait_for_log(log_file=log, string_list=strings)

        Helpers.android_screen_match(image=self.image_original, timeout=120)

    def test_006_ios_run_hmr_console_log(self):
        source_js = os.path.join('data', "issues", 'console-log-hmr', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                                assert_success=False)
        strings = ['JS: LOG']
        Tns.wait_for_log(log_file=log, string_list=strings)

        Helpers.ios_screen_match(image=self.image_original, timeout=120)

    # def test_007_android_run_hmr_delete_file(self):
    #     log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
    #                     assert_success=False)
    #
    #     Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
    #                      timeout=240)
    #     Helpers.android_screen_match(image=self.image_original, timeout=120)
    #     File.remove(self.app_name + 'app', 'main-view-model.js')
    #
    #     self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
    #     self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
import unittest

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


class WebPackHelloWorldJS(BaseClass):
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

        # Change JS, XML and CSS
        ReplaceHelper.replace(app_name, WebPackHelloWorldJS.js_change, sleep=10)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, WebPackHelloWorldJS.xml_change, sleep=10)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, WebPackHelloWorldJS.css_change, sleep=10)
        if platform == Platform.ANDROID:
            Tns.wait_for_log(log_file=log, string_list=['app.css'], clean_log=False)

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=120)

        # Verify application looks correct
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=WebPackHelloWorldJS.image_change, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=WebPackHelloWorldJS.SIMULATOR_ID, image=WebPackHelloWorldJS.image_change,
                                     timeout=120)

    @staticmethod
    def revert_changes(app_name, log, platform):
        # Clean old logs
        if CURRENT_OS is not OSType.WINDOWS:
            File.write(file_path=log, text="")

        # Revert XML changes
        ReplaceHelper.rollback(app_name, WebPackHelloWorldJS.xml_change, sleep=10)
        Tns.wait_for_log(log_file=log, string_list=['main-page.xml'], clean_log=False)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TAP')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Revert JS changes
        ReplaceHelper.rollback(app_name, WebPackHelloWorldJS.js_change, sleep=10)
        Tns.wait_for_log(log_file=log, string_list=['main-view-model.js'], clean_log=False)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left', timeout=20)
            assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Revert CSS changes
        ReplaceHelper.rollback(app_name, WebPackHelloWorldJS.css_change, sleep=10)
        Tns.wait_for_log(log_file=log, string_list=['app.css'], clean_log=False)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors,
                         timeout=60)
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=WebPackHelloWorldJS.image_original, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=WebPackHelloWorldJS.SIMULATOR_ID, image=WebPackHelloWorldJS.image_original,
                                     timeout=120)

    def test_001_android_run_hmr(self):
        log = Tns.run_android(attributes={"--path": self.app_name})

        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.android_screen_match(image=self.image_original, timeout=120)
        Helpers.wait_webpack_watcher()
import os
import time
import unittest

from flaky import flaky

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.preview_app.preview import Preview
from core.settings.settings import SUT_FOLDER, SIMULATOR_NAME, TEST_RUN_HOME, WEBPACK_PACKAGE, \
    EMULATOR_ID, EMULATOR_NAME, EMULATOR_PORT, USE_YARN
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class PreviewCommandTestsIos(BaseClass):
    SIMULATOR_ID = ''
    app_webpack_name = "TestAppWebpack"
    app_angular_name = "TestAppNG"
    css_change_webpack = ['app/app.css', '18', '32']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.kill()
        Simulator.stop()
        Emulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.IOS)

        Preview.get_app_packages()
        Preview.install_preview_app(cls.SIMULATOR_ID, platform=Platform.IOS)
        Preview.install_playground_app(cls.SIMULATOR_ID, platform=Platform.IOS)

        Tns.create_app(BaseClass.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

        """We need new project because we need app with long imports to test preview with --bundle"""
        Tns.create_app(cls.app_webpack_name,
                       attributes={"--template": os.path.join(SUT_FOLDER, "template-hello-world")})
        if USE_YARN == "True":
            Tns.install_npm(package=WEBPACK_PACKAGE, option='--dev', folder=cls.app_webpack_name)
        else:
            Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=cls.app_webpack_name)
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_webpack_name, TEST_RUN_HOME + "/data/TestAppWebpack")

        """Create angular app"""
        Tns.create_app_ng(cls.app_angular_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")

    def setUp(self):
        BaseClass.setUp(self)
        Folder.navigate_to(folder=TEST_RUN_HOME, relative_from_current_folder=False)
        Folder.cleanup(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @flaky(max_runs=3)
    def test_001_tns_preview_ios_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                          log_trace=True, assert_success=False)

        strings = [
            'Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        output = File.read(log)
        url = Preview.get_url(output)

        Preview.run_app(url, self.SIMULATOR_ID, platform=Platform.IOS)
        """On ios simulator allert which has to be accepted is shown first, so we need to dissmiss it"""
        time.sleep(2)
        Preview.dismiss_simulator_alert()

        strings = ['Start sending initial files for platform ios',
                   'Successfully sent initial files for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home', timeout=60)

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Start syncing changes for platform ios', 'Successfully synced main-view-model.js for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Start syncing changes for platform ios', 'Successfully synced main-page.xml for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Start syncing changes for platform ios', 'Successfully synced app.css for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml', timeout=60)

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Start syncing changes for platform ios', 'Successfully synced main-view-model.js for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Start syncing changes for platform ios', 'Successfully synced app.css for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Start syncing changes for platform ios', 'Successfully synced main-page.xml for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home', timeout=6)

    @flaky(max_runs=3)
    def test_002_tns_preview_ios_webpack_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # Ensure app is in initial state 
        Folder.cleanup(self.app_webpack_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestAppWebpack", TEST_RUN_HOME + "/TestAppWebpack")

        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_webpack_name, '--bundle': ''}, wait=False,
                          log_trace=True, assert_success=False)
        strings = [
            'Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, self.SIMULATOR_ID, platform=Platform.IOS)

        strings = ['Running webpack for ios',
                   'Webpack build done',
                   'Start sending initial files for platform ios',
                   'Successfully sent initial files for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-js')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_webpack_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=self.SIMULATOR_ID, text='42 clicks left')
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_webpack_name, self.css_change_webpack, sleep=3)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_webpack_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=self.SIMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-js-js-css-xml')

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_webpack_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_webpack_name, self.css_change_webpack, sleep=3)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_webpack_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-js')

    def test_003_tns_preview_ios_ng_webpack_ts_css_html(self):
        """Make valid changes in TS,CSS and HTML"""

        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_angular_name, '--bundle': ''}, wait=False,
                          log_trace=True, assert_success=False)
        strings = [
            'Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, self.SIMULATOR_ID, platform=Platform.IOS)

        strings = ['Running webpack for ios',
                   'Webpack build done',
                   'Start sending initial files for platform ios',
                   'Successfully sent initial files for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        Device.wait_for_text(device_id=self.SIMULATOR_ID, text="Ter Stegen", timeout=20)
        # Verify app looks correct inside emulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-ng-preview')

        # Change TS and wait until app is synced
        ReplaceHelper.replace(self.app_angular_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done',
                   'Successfully synced']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)
        text_changed = Device.wait_for_text(device_id=self.SIMULATOR_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Change HTML and wait until app is synced
        ReplaceHelper.replace(self.app_angular_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)

        # Verify app is synced 
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done',
                   'Successfully synced']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=self.SIMULATOR_ID, text='11')
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_angular_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)

        # Verify app is synced 
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done',
                   'Successfully synced']
        Tns.wait_for_log(log_file=log, string_list=strings)
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='ng-hello-world-home-dark_preview',
                            tolerance=5.0)

        # Revert TS and wait until app is synced
        ReplaceHelper.rollback(self.app_angular_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done',
                   'Successfully synced']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Revert HTML and wait until app is synced
        ReplaceHelper.rollback(self.app_angular_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done',
                   'Successfully synced']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Revert CSS and wait until app is synced
        ReplaceHelper.rollback(self.app_angular_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done',
                   'Successfully synced']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-ng-preview', tolerance=5.0)

    @unittest.skip("Skip because of https://github.com/NativeScript/ios-runtime/issues/1009")
    def test_180_tns_preview_ios_console_logging(self):
        """
         Test console info, warn, error, assert, trace, time and logging of different objects.
        """
        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                          log_trace=True, assert_success=False)
        strings = [
            'Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, self.SIMULATOR_ID, platform=Platform.IOS)

        strings = ['Start sending initial files for platform ios',
                   'Successfully sent initial files for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-log', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        strings = ['Start syncing changes for platform ios',
                   'Successfully synced main-page.js for platform ios',
                   "CONSOLE LOG",
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   "number: -1",
                   "string: text",
                   "text -1",
                   "CONSOLE INFO",
                   "info",
                   "CONSOLE WARN",
                   "warn",
                   "CONSOLE ERROR",
                   "error",
                   "false == true",
                   "empty string evaluates to 'false'",
                   "CONSOLE TRACE",
                   "console.trace() called",
                   "0: pageLoaded",
                   "Button(8)",
                   "-1 text {",
                   "CONSOLE INFO Time:",
                   "### TEST END ###"
                   ]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home_preview')

    @flaky(max_runs=3)
    def test_185_tns_preview_on_both_platforms(self):
        """Open project in Preview on both ios and android emulators"""
        # Start android emulator and install Preview App
        Emulator.start(emulator_name=EMULATOR_NAME, port=EMULATOR_PORT)
        Preview.install_preview_app(EMULATOR_ID, platform=Platform.ANDROID)

        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                          log_trace=True, assert_success=False)

        strings = [
            'Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        output = File.read(log)
        url = Preview.get_url(output)

        Preview.run_app(url, self.SIMULATOR_ID, platform=Platform.IOS)
        """On ios simulator allert which has to be accepted is shown first, so we need to dissmiss it"""
        time.sleep(2)
        Preview.dismiss_simulator_alert()

        strings = ['Start sending initial files for platform ios',
                   'Successfully sent initial files for platform ios']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home', timeout=60)

        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)

        strings = ['Start sending initial files for platform android',
                   'Successfully sent initial files for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home_preview')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Start syncing changes for platform ios',
                   'Successfully synced main-view-model.js for platform ios',
                   'Start syncing changes for platform android',
                   'Successfully synced main-view-model.js for platform android'
                   ]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Start syncing changes for platform ios',
                   'Successfully synced main-page.xml for platform ios',
                   'Start syncing changes for platform android',
                   'Successfully synced main-page.xml for platform android'
                   ]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Start syncing changes for platform ios',
                   'Successfully synced app.css for platform ios',
                   'Start syncing changes for platform android',
                   'Successfully synced app.css for platform android'
                   ]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml_preview')

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_js_css_xml', timeout=6)

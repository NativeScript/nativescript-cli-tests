import os

from core.base_class.BaseClass import BaseClass

from core.preview_app.preview import Preview

from core.device.emulator import Emulator

from core.tns.tns import Tns

from core.device.device import Device

from core.osutils.file import File

from core.osutils.folder import Folder

from core.tns.tns_platform_type import Platform

from core.tns.replace_helper import ReplaceHelper

from core.settings.settings import TEST_RUN_HOME, EMULATOR_ID, EMULATOR_NAME, WEBPACK_PACKAGE,SUT_FOLDER

class PreviewCommandTestsAndroid(BaseClass):
    app_webpack_name = "TestAppWebpack"
    css_change_webpack = ['app/app.css', '18', '32']
    EMULATOR_ID_SECOND = "emulator-5556"
    EMULATOR_NAME_SECOND = "Emulator-Api24-Default"
    EMULATOR_PORT_SECOND = "5556"


    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.kill()
        Emulator.stop()
        Emulator.ensure_available()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

        Preview.get_app_packages()
        Preview.install_preview_app(EMULATOR_ID, platform=Platform.ANDROID)

        Tns.create_app(BaseClass.app_name,
                           attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                           update_modules=True)
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

        """We need new project because we need app with long imports to test preview with --bundle"""
        Tns.create_app(cls.app_webpack_name,attributes={"--template": os.path.join(SUT_FOLDER, "template-hello-world")})
        Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=cls.app_webpack_name)

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

    def test_001_tns_preview_android_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        strings = ['Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Start syncing changes for platform android',
                   'Project successfully prepared (android)',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home_preview')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Start syncing changes for platform android', 'Successfully synced main-view-model.js for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=30)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Start syncing changes for platform android', 'Successfully synced app.css for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Start syncing changes for platform android', 'Successfully synced main-page.xml for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Verify application looks correct
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml_preview')

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Start syncing changes for platform android', 'Successfully synced main-view-model.js for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Start syncing changes for platform android', 'Successfully synced app.css for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Start syncing changes for platform android', 'Successfully synced main-page.xml for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        #Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home_preview')

    def test_002_tns_preview_android_webpack_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""
        
        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_webpack_name,'--bundle':'' }, wait=False,
                        log_trace=True,assert_success=False)
        strings = ['Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Running webpack for android',
                   'Webpack build done',
                   'Start syncing changes for platform android',
                   'Project successfully prepared (android)',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_webpack_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left')
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_webpack_name, self.css_change_webpack, sleep=3)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)
        
        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_webpack_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['File change detected. Starting incremental webpack compilation', 'Webpack build done']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Verify application looks correct
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
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

        #Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    def test_180_tns_preview_android_console_logging(self):
        """
         Test console info, warn, error, assert, trace, time and logging of different objects.
        """
         # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        strings = ['Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Start syncing changes for platform android',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-log', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)
        
        strings = ['Start syncing changes for platform android',
                   'Successfully synced main-page.js for platform android',
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   "\"name\": \"John\",",
                   "\"age\": 34",
                   "number: -1",
                   "string: text",
                   "text -1",
                   "info",
                   "warn",
                   "error",
                   "Assertion failed:  false == true",
                   "Assertion failed:  empty string evaluates to 'false'",
                   "Trace: console.trace() called",
                   "at pageLoaded",
                   "Button(8)",
                   "-1 text {",
                   "[1, 5, 12.5, {", "\"name\": \"John\",",
                   "\"age\": 34",
                   "}, text, 42]",
                   "Time:",
                   "### TEST END ###"
                   ]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home_preview')

    def test_185_tns_preview_android_verify_plugin_warrnings(self):
        """
         Test if correct messages are showh if plugin is missing or versions differ in Preview App.
        """
        # `tns preview` and take the app url and open it in Preview App
        Tns.plugin_add("nativescript-barcodescanner", attributes={"--path": self.app_name})
        Tns.plugin_add("nativescript-geolocation@3.0.1", attributes={"--path": self.app_name})
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        strings = ['Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Start syncing changes for platform android',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Verify warnings for plugins
        strings = ['Plugin nativescript-barcodescanner is not included in preview app on device {0} and will not work'.format(EMULATOR_ID), 
                   'Local plugin nativescript-geolocation differs in major version from plugin in preview app',
                   'Some features might not work as expected'
                  ]
    
    def test_190_tns_preview_android_check_only_one_emulator_refreshed(self):
        """
         When scanning QR code on multiple devices verify that only the current device is refreshed
        """
        # Start second emulator and install Preview on it
        Emulator.start(self.EMULATOR_NAME_SECOND, self.EMULATOR_PORT_SECOND)
        Preview.install_preview_app(self.EMULATOR_ID_SECOND, platform=Platform.ANDROID)

        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        strings = ['Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Start syncing changes for platform android',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=True)

        # Tap on the button and verify the change in the app 
        Device.click(device_id=EMULATOR_ID, text="TAP", timeout=30)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_preview_after_tap', timeout=15)
        
        # Run app in Preview on second emulator
        Preview.run_app(url, self.EMULATOR_ID_SECOND, platform=Platform.ANDROID)
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Verify app on first emulator in not reloaded
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_preview_after_tap', timeout=15)


    def test_195_tns_preview_android_livesync_on_two_emulators(self):
        """ 
         Scan QR code on two emulators and veify livesync on them
        """ 
        # `tns preview` and take the app url and open it in Preview App
        log = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        strings = ['Use NativeScript Playground app and scan the QR code above to preview the application on your device']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(log)
        url = Preview.get_url(output)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Start syncing changes for platform android',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=True)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home_preview')

        # Run app in Preview on second emulator
        Preview.run_app(url, self.EMULATOR_ID_SECOND, platform=Platform.ANDROID)
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=True)
        
        # Verify app looks correct inside emulator
        Device.screen_match(device_name="Emulator-Api24-Default", device_id="emulator-5556",
                            expected_image='livesync-hello-world_home_preview')

        # Change JS file
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Start syncing changes for platform android', 'Successfully synced main-view-model.js for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app is synced on first emulator
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=30)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Verify app is synced on second emulator
        text_changed = Device.wait_for_text(device_id=self.EMULATOR_ID_SECOND, text='42 clicks left', timeout=30)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

    
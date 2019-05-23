"""
Test for `tns run android` command on Angular projects

Run should sync all the changes correctly:
 - Valid changes in CSS, TS, HTML should be applied.
"""

import os

from flaky import flaky

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_PACKAGE, EMULATOR_ID, EMULATOR_NAME, CURRENT_OS
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class RunAndroidEmulatorTestsNG(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

        # Create default NG app (to get right dependencies from package.json)
        Tns.create_app_ng(cls.app_name)
        Tns.platform_add_android(attributes={'--path': cls.app_name, '--frameworkPath': ANDROID_PACKAGE}) 

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_200_tns_run_android_extending_class_inside_file_containing_dots(self):
        """Test for https://github.com/NativeScript/android-runtime/issues/761"""

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'src')
        target = os.path.join(self.app_name, 'src')
        Folder.cleanup(target)
        Folder.copy(src=source, dst=target)
        
        source_html = os.path.join('data', 'issues', 'android-runtime-761', 'items.component.html')
        target_html = os.path.join(self.app_name, 'src', 'app', 'item', 'items.component.html')
        File.copy(src=source_html, dest=target_html)

        source_ts = os.path.join('data', 'issues', 'android-runtime-761', 'items.component.ts')
        target_ts = os.path.join(self.app_name, 'src', 'app', 'item', 'items.component.ts')
        File.copy(src=source_ts, dest=target_ts)

        source_xml = os.path.join('data', 'issues', 'android-runtime-761', 'AndroidManifest.xml')
        target_xml = os.path.join(self.app_name, 'App_Resources', 'Android', 'src', 'main', 'AndroidManifest.xml')
        File.copy(src=source_xml, dest=target_xml)

        # Verify the app is running
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

    def test_280_tns_run_android_console_time(self):
        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'src')
        target = os.path.join(self.app_name, 'src')
        Folder.cleanup(target)
        Folder.copy(src=source, dst=target)

        # Replace app.component.ts to use console.time() and console.timeEnd()
        source = os.path.join('data', 'issues', 'ios-runtime-843', 'app.component.ts')
        target = os.path.join(self.app_name, 'src', 'app', 'app.component.ts')
        File.copy(src=source, dest=target)

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)

        # Verify the app is running
        strings = ['Successfully synced application',
                   'Application loaded!',
                   'Home page loaded!']

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Verify initial state of the app
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='ng-hello-world-home-white', tolerance=5.0)

        # Verify console.time() works
        console_time = ['JS: startup:']
        Tns.wait_for_log(log_file=log, string_list=console_time)

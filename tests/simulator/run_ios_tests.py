"""
Test for `tns run ios` command.

Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sync should continue when XML is fixed.
 - Hidden files should not be synced at all.
 - --syncAllFiles should sync changes in node_modules
 - --justlaunch should release the console.

If simulator is not started and device is not connected `tns run ios` should start simulator.
"""

import os
import time
import unittest

import nose

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.device_type import DeviceType
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunIOSSimulatorTests(BaseClass):
    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.start(name=SIMULATOR_NAME)
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

    def tearDown(self):
        Process.kill('node')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_tns_run_ios_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_js_css_xml')

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside simulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_200_tns_run_ios_break_and_fix_app(self):
        """
        Make changes in xml that break the app and then changes that fix the app.
        """

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Break the app with invalid xml changes
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)

        # Verify console notify user for broken xml
        strings = ['main-page.xml has syntax errors', 'unclosed xml attribute',
                   'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Revert changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_210_tns_run_ios_add_remove_files_and_folders(self):
        """
        New files and folders should be synced properly.
        """

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False,
                          assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Add new files
        new_file_name = 'main-page2.xml'
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', new_file_name)
        File.copy(source_file, destination_file)
        strings = ['Successfully transferred', 'main-page2.xml', 'Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is synced and available on device.
        error_message = 'Newly created file {0} not found on {1}'.format(new_file_name, self.SIMULATOR_ID)
        app_id = Tns.get_app_id(app_name=self.app_name)
        path = 'app/{0}'.format(new_file_name)
        assert Simulator.path_exists(package_id=app_id, path=path), error_message

        # Revert changes(rename file and delete file)
        File.copy(destination_file, source_file)
        File.remove(destination_file)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is synced and available on device.
        error_message = '{0} was deleted, but still available on {1}'.format(new_file_name, self.SIMULATOR_ID)
        assert Simulator.path_does_not_exist(package_id=app_id, path=path), error_message

        # Add folder
        new_folder_name = 'test2'
        source_file = os.path.join(self.app_name, 'app', 'test')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred', 'test2', 'Successfully transferred', 'test.txt', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is synced and available on device.
        error_message = 'Newly created folder {0} not found on {1}'.format(new_folder_name, self.SIMULATOR_ID)
        path = 'app/{0}'.format(new_folder_name)
        assert Simulator.path_exists(package_id=app_id, path=path), error_message

        # Delete folder
        Folder.cleanup(destination_file)
        strings = ['Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is sysched and available on device.
        error_message = 'Deleted folder {0} is still available on {1}'.format(new_folder_name, self.SIMULATOR_ID)
        assert Simulator.path_does_not_exist(package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_300_tns_run_ios_just_launch_and_incremental_builds(self):
        """
        This test verify following things:
        1. `--justlaunch` option release the console.
        2. Prepare is not triggered if no changed are done.
        3. Incremental prepare is triggered if js, xml and css files are changed.
        """

        # Execute `tns run android --path TNS_App --justlaunch` and verify app looks correct on emulator
        Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''}, timeout=120)
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Execute `tns run android --path TNS_App --justlaunch` again
        # without any changes on app under test and verify incremental prepare works
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False, timeout=30)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.SKIP)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Replace JS, XML and CSS files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML)

        # Run `tns run android` after file changes (this should trigger incremental prepare).
        output = Tns.run_ios(attributes={'--path': self.app_name, '--justlaunch': ''}, assert_success=False, timeout=60)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.INCREMENTAL)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_js_css_xml')

    def test_330_tns_run_ios_sync_all_files(self):
        """
        Verify '--syncAllFiles' option will sync all files, including node modules.
        """
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--syncAllFiles': ''},
                          wait=False, assert_success=False)
        strings = ['Successfully installed on device with identifier',
                   'Successfully synced application',
                   self.SIMULATOR_ID,  # Verify device id
                   'CONSOLE LOG']  # Verify console log messages are shown.
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        ReplaceHelper.replace(app_name=self.app_name, file_change=ReplaceHelper.CHANGE_TNS_MODULES)

        strings = ['Successfully transferred', 'application-common.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside simulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/2642")
    def test_340_tns_run_should_not_sync_hidden_files(self):
        """
        Adding hidden files should not break run and they should not be transferred.
        """

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        sync_message = 'Successfully synced application {0} on device {1}' \
            .format(Tns.get_app_id(self.app_name), self.SIMULATOR_ID)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', sync_message]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Add some hidden files
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', '.tempfile')
        File.copy(source_file, destination_file)
        time.sleep(10)
        strings = ['Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify hidden file does not exists on mobile device.
        path = 'app/{0}'.format('.tempfile')
        app_id = Tns.get_app_id(self.app_name)
        error_message = 'Hidden file {0} is transferred to {1}'.format(path, self.SIMULATOR_ID)
        assert Simulator.path_does_not_exist(package_id=app_id, path=path), error_message

        # Verify app looks correct inside simulator
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_350_tns_run_ios_should_start_simulator(self):
        """
        `tns run ios` should start iOS Simulator if device is not connected.
        """
        count = Device.get_count(platform='ios')
        if count == 0:
            Simulator.stop()
            Tns.run_ios(attributes={'--path': self.app_name, '--justlaunch': ''})
            assert Simulator.wait_for_simulator(timeout=10), 'iOS Simulator not started by `tns run ios`!'
        else:
            raise nose.SkipTest('This test is not valid when devices are connected.')

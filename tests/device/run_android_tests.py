"""
Test for `tns run android` command (on real devices).

Verify `tns run android`
- Run on all available devices
- Changes are synced on physical devices
- Emulator is not started if physical device is attached
- `tns run android --emulator` starts emulator even if device is connected
- `tns run android --emulator` should deploy only on emulator
- `tns run android --device` should deploy only on specified device

TODO: Add tests for:
`tns run android --device <avd-name>` -> Should be able to start avd image
`tns run android --device --emulator` -> We should throw nice error
`--available-devices` and `-timeout` options
"""

import os

from core.base_class.BaseClass import BaseClass
from core.device.adb import Adb
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunAndroidDeviceTests(BaseClass):
    DEVICES = Device.get_ids(platform=Platform.ANDROID)
    DEVICE_ID = Device.get_id(platform=Platform.ANDROID)

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Device.ensure_available(platform=Platform.ANDROID)
        Folder.cleanup(cls.app_name)
        Tns.create_app(cls.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': cls.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Process.kill(proc_name='node')  # Stop 'node' to kill the livesync after each test method.

    def tearDown(self):
        Process.kill(proc_name='node')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_tns_run_android_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Verify app is deployed and running on all available android devices
        output = File.read(log)
        for device_id in self.DEVICES:
            assert device_id in output, 'Application is not deployed on {0}'.format(device_id)
            Device.wait_until_app_is_running(app_id=Tns.get_app_id(self.app_name), device_id=device_id, timeout=30)

        # Verify emulator is not started
        assert not Emulator.is_running(EMULATOR_ID), \
            'Device is attached, but emulator is also started after `tns run android`!'

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Adb.wait_for_text(device_id=self.DEVICE_ID, text='clicks', timeout=20)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Adb.wait_for_text(device_id=self.DEVICE_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Assert changes are reverted
        assert Adb.wait_for_text(device_id=self.DEVICE_ID, text='TAP'), 'Changes in XML file not reverted.'
        assert Adb.wait_for_text(device_id=self.DEVICE_ID, text='taps'), 'Changes in JS file not reverted.'

    def test_210_tns_run_android_add_remove_files_and_folders(self):
        """
        New files and folders should be synced properly.
        """

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': self.DEVICE_ID}, wait=False,
                              assert_success=False)
        strings = ['Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Add new files
        new_file_name = 'main-page2.xml'
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', new_file_name)
        File.copy(source_file, destination_file)
        strings = ['Successfully transferred main-page2.xml', 'Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is synced and available on device.
        error_message = 'Newly created file {0} not found on {1}'.format(new_file_name, self.DEVICE_ID)
        app_id = Tns.get_app_id(app_name=self.app_name)
        path = 'app/{0}'.format(new_file_name)
        assert Adb.path_exists(device_id=self.DEVICE_ID, package_id=app_id, path=path), error_message

        # Revert changes(rename file and delete file)
        File.copy(destination_file, source_file)
        File.remove(destination_file)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is synced and available on device.
        error_message = '{0} was deleted, but still available on {1}'.format(new_file_name, self.DEVICE_ID)
        assert Adb.path_does_not_exist(device_id=self.DEVICE_ID, package_id=app_id, path=path), error_message

        # Add folder
        new_folder_name = 'feature2'
        source_file = os.path.join(self.app_name, 'app', 'feature1')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred', 'Successfully transferred', 'feature2', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is synced and available on device.
        error_message = 'Newly created folder {0} not found on {1}'.format(new_folder_name, self.DEVICE_ID)
        path = 'app/{0}'.format(new_folder_name)
        assert Adb.path_exists(device_id=self.DEVICE_ID, package_id=app_id, path=path, timeout=20), error_message
        path = 'app/{0}/{1}'.format(new_folder_name, 'feature1.js')
        assert Adb.path_exists(device_id=self.DEVICE_ID, package_id=app_id, path=path, timeout=20), error_message

        # Delete folder
        Folder.cleanup(destination_file)
        strings = ['Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is synced and available on device.
        error_message = 'Deleted folder {0} is still available on {1}'.format(new_folder_name, self.DEVICE_ID)
        assert Adb.path_does_not_exist(device_id=self.DEVICE_ID, package_id=app_id, path=path), error_message

        # Add same folder again
        new_folder_name = 'feature2'
        source_file = os.path.join(self.app_name, 'app', 'feature1')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred', 'Successfully transferred', 'feature2', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is synced and available on device.
        error_message = 'Newly created folder {0} not found on {1}'.format(new_folder_name, self.DEVICE_ID)
        path = 'app/{0}'.format(new_folder_name)
        assert Adb.path_exists(device_id=self.DEVICE_ID, package_id=app_id, path=path, timeout=20), error_message
        path = 'app/{0}/{1}'.format(new_folder_name, 'feature1.js')
        assert Adb.path_exists(device_id=self.DEVICE_ID, package_id=app_id, path=path, timeout=20), error_message

    def test_300_tns_run_android_emulator_should_start_emulator_even_if_device_is_connected(self):
        """
        `tns run android --emulator` should start emulator even if physical device is connected
        """
        Emulator.stop()
        output = Tns.run_android(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                                 assert_success=False)
        assert 'Starting Android emulator with image' in output
        assert Emulator.is_running(device_id=EMULATOR_ID), 'Emulator not started by `tns run android`!'

    def test_310_tns_run_android_emulator_should_run_only_on_emulator(self):
        """
        `tns run android --emulator` should start emulator even if physical device is connected
        """
        Emulator.ensure_available()
        output = Tns.run_android(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                                 assert_success=False)
        assert 'Starting Android emulator with image' not in output
        assert EMULATOR_ID in output
        for device_id in self.DEVICES:
            assert device_id not in output, 'Application is deployed on {0} device.'.format(device_id)

    def test_320_tns_run_android_specific_device(self):
        """
        `tns run android --device` should run only on specified device
        """
        Emulator.ensure_available()
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': self.DEVICE_ID, '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.ANDROID, prepare=Prepare.SKIP)
        assert EMULATOR_ID not in output, 'Application is also deployed on emulator!'
        for device_id in self.DEVICES:
            if device_id != self.DEVICE_ID:
                assert device_id not in output, \
                    'Application is deployed on {0} while it should be only on {1}'.format(device_id, self.DEVICES)

        output = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.ANDROID, prepare=Prepare.SKIP)
        assert EMULATOR_ID in output, 'Application is NOT deployed on emulator specified by --device option!'
        for device_id in self.DEVICES:
            assert device_id not in output, \
                'Application is deployed on {0} while it should be only on {1}'.format(device_id, EMULATOR_ID)

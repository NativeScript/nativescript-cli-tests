"""
Test for `tns run android` command.

Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sync should continue when XML is fixed.
 - Hidden files should not be synced at all.
 - --syncAllFiles should sync changes in node_modules
 - --justlaunch should release the console.

If emulator is not started and device is not connected `tns run android` should start emulator.
"""

import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID, EMULATOR_NAME
from core.tns.tns import Tns


class TemplateAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Process.kill('node')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    @parameterized.expand([
        "nativescript-template-tutorial",
        "nativescript-template-ng-tutorial",
        "template-drawer-navigation-ts",
        "template-tab-navigation-ts",
        "template-master-detail-ng",
        "template-drawer-navigation",
        "template-master-detail-ts",
        "template-tab-navigation",
        "template-drawer-navigation-ng",
        "template-master-detail",
        "template-tab-navigation-ng",
    ])
    def test_100_templates_android(self, template_source):
        """Tests for {N} templates"""

        # Create application
        url = "https://github.com/NativeScript/" + template_source
        Tns.create_app(self.app_name, attributes={"--template": url}, update_modules=False)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

        # Start it
        Tns.run_android(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''})

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=template_source + "_home")

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
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class TemplateIOSTests(BaseClass):
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

    def tearDown(self):
        Tns.kill()
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
    def test_100_templates_ios(self, template_source):

        # Create application
        url = "https://github.com/NativeScript/" + template_source
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name, attributes={"--template": url}, update_modules=False)
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

        # Build it
        Tns.build_ios(attributes={'--path': self.app_name})

        # Start it
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        assert "Successfully synced application" in output, "Failed to run the app!"

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image=template_source + '_home')

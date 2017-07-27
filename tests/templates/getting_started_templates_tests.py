"""
Verify getting started templates looks ok
"""

import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID, EMULATOR_NAME, IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class GettingStartedTemplatesTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
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
    ])
    def test_100_templates_android(self, template_source):

        # Create application
        url = "https://github.com/NativeScript/" + template_source
        Tns.create_app(self.app_name, attributes={"--template": url}, assert_success=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

        # Build it
        Tns.build_android(attributes={'--path': self.app_name})
        Tns.build_ios(attributes={'--path': self.app_name})

        # Verify Android looks ok
        output = Tns.run_android(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                                 assert_success=False)
        assert "Successfully synced application" in output, "Failed to run the app!"
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=template_source + "_home")

        # Verify iOS looks ok
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        assert "Successfully synced application" in output, "Failed to run the app!"
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image=template_source + '_home')

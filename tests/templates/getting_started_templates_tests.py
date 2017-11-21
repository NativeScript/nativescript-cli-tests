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
        Simulator.stop()
        Emulator.ensure_available()
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
        ('t-js-live-template-live-n', 'nativescript-template-tutorial', False),
        ('t-js-live-template-next-n', 'nativescript-template-tutorial', True),
        ('t-js-next-template-next-n', 'https://github.com/NativeScript/nativescript-template-tutorial', True),
        ('t-ng-live-template-live-n', 'nativescript-template-ng-tutorial', False),
        ('t-ng-live-template-next-n', 'nativescript-template-ng-tutorial', True),
        ('t-ng-next-template-next-n', 'https://github.com/NativeScript/nativescript-template-ng-tutorial', True),
    ])
    def test(self, description, url, update):
        # Create application
        Tns.create_app(self.app_name, attributes={"--template": url}, assert_success=True, update_modules=update)
        if update:
            Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})
            Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_RUNTIME_PATH})
        else:
            Tns.platform_add_android(attributes={'--path': self.app_name}, version="latest")
            Tns.platform_add_ios(attributes={'--path': self.app_name}, version="latest")

        # Build it
        Tns.build_android(attributes={'--path': self.app_name})
        Tns.build_ios(attributes={'--path': self.app_name})

        # Verify Android looks ok
        output = Tns.run_android(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                                 assert_success=False)
        assert "Successfully synced application" in output, "Failed to run the app!"
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=description, tolerance=3.0)

        # Verify iOS looks ok
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        assert "Successfully synced application" in output, "Failed to run the app!"
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID, expected_image=description,
                            tolerance=3.0)

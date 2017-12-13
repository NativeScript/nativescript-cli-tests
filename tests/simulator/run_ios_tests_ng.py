"""
Test for `tns run ios` command with Angular apps (on simulator).
"""

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class RunIOSSimulatorTestsNG(BaseClass):
    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(cls.app_name)

        # Create default NG app (to get right dependencies from package.json)
        Tns.create_app_ng(cls.app_name)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'app')
        target = os.path.join(cls.app_name, 'app')
        Folder.cleanup(target)
        Folder.copy(src=source, dst=target)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.kill()

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_tns_run_ios(self):
        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False,
                          assert_success=False)
        strings = ['Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Verify initial state of the app
        assert Device.wait_for_text(device_id=self.SIMULATOR_ID, text="Ter Stegen",
                                    timeout=20), 'Hello-world NG App failed to start or it does not look correct!'

        # Verify console.log works - issue #3141
        console_log_strings = ['CONSOLE LOG', 'Home page loaded!', 'Application loaded!']
        Tns.wait_for_log(log_file=log, string_list=console_log_strings, clean_log=False)

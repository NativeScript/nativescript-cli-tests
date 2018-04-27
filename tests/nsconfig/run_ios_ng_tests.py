"""
Test for `tns run ios` command with Angular apps (on simulator).
"""

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class RunIOSSimulatorTestsNG(BaseClass):
    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS"):
            assert "ChangeAppLocationLSNG" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS", TEST_RUN_HOME + "/ChangeAppLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLS",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLSNG", TEST_RUN_HOME + "/ChangeAppResLocationLSNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLSNG",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRootLSNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppLSNG", TEST_RUN_HOME + "/RenameAppLSNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResLSNG", TEST_RUN_HOME + "/RenameAppResLSNG")
        else:
            CreateNSConfigApps.createAppsLiveSyncNG(cls.__name__)
            if not File.exists(TEST_RUN_HOME + "/ChangeAppLocationLSNG"):
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLSNG", TEST_RUN_HOME + "/ChangeAppLocationLSNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLSNG",
                            TEST_RUN_HOME + "/ChangeAppLocationAndNameLSNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLSNG", TEST_RUN_HOME + "/ChangeAppResLocationLSNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLSNG",
                            TEST_RUN_HOME + "/ChangeAppResLocationInRootLSNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppLSNG", TEST_RUN_HOME + "/RenameAppLSNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResLSNG", TEST_RUN_HOME + "/RenameAppResLSNG")
            else:
                assert "ChangeAppLocationLSNG" in TEST_RUN_HOME + "/"

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)
        
    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

        Folder.cleanup("ChangeAppLocationLSNG")
        Folder.cleanup("ChangeAppLocationAndNameLSNG")
        Folder.cleanup("ChangeAppResLocationLSNG")
        Folder.cleanup("ChangeAppResLocationInRootLSNG")
        Folder.cleanup("RenameAppLSNG")
        Folder.cleanup("RenameAppResLSNG")
        Folder.cleanup("ChangeAppLocationLSNG.app")
        File.remove("ChangeAppLocationLSNG.ipa")
        Folder.cleanup("ChangeAppLocationAndNameLSNG.app")
        File.remove("ChangeAppLocationAndNameLSNG.ipa")
        Folder.cleanup("ChangeAppResLocationLSNG.app")
        File.remove("ChangeAppResLocationLSNG.ipa")
        Folder.cleanup("ChangeAppResLocationInRootLSNG.app")
        File.remove("ChangeAppResLocationInRootLSNG.ipa")
        Folder.cleanup("RenameAppLSNG.app")
        File.remove("RenameAppLSNG.ipa")
        Folder.cleanup("RenameAppResLSNG.app")
        File.remove("RenameAppResLSNG.ipa")

    @parameterized.expand([
        'ChangeAppLocationLSNG',
        'ChangeAppLocationAndNameLSNG',
        'ChangeAppResLocationLSNG',
        'ChangeAppResLocationInRootLSNG',
        'RenameAppLSNG',
        'RenameAppResLSNG'
    ])
    def test_001_tns_run_ios(self, app_name):
        # `tns run ios` and wait until app is deployed
        Tns.build_ios(attributes={'--path': app_name})
        log = Tns.run_ios(attributes={'--path': app_name, '--emulator': ''}, wait=False,
                          assert_success=False)
        strings = ['Successfully synced application', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=90, check_interval=10, clean_log=False)

        # Verify initial state of the app
        assert Device.wait_for_text(device_id=self.SIMULATOR_ID, text="Ter Stegen",
                                    timeout=20), 'Hello-world NG App failed to start or it does not look correct!'

        # Verify console.log works - issue #3141
        console_log_strings = ['CONSOLE LOG', 'Home page loaded!', 'Application loaded!']
        Tns.wait_for_log(log_file=log, string_list=console_log_strings)

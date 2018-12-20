"""
Test for `tns run ios` command with different nsconfig setup.
Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sync should continue when XML is fixed.
 - Hidden files should not be synced at all.
 - --syncAllFiles should sync changes in node_modules
 - --justlaunch should release the console.
If simulator is not started and device is not connected `tns run ios` should start simulator.
"""

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import SIMULATOR_NAME
from core.settings.settings import TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class RunIOSSimulatorTests(BaseClass):
    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS"):
            assert "ChangeAppLocationLS" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS", TEST_RUN_HOME + "/ChangeAppLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLS",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRootLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppLS", TEST_RUN_HOME + "/RenameAppLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResLS", TEST_RUN_HOME + "/RenameAppResLS")
        else:
            CreateNSConfigApps.createAppsLiveSync()

        if not File.exists(TEST_RUN_HOME + "/ChangeAppLocationLS"):
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS",
                        TEST_RUN_HOME + "/ChangeAppLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLS",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRootLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppLS", TEST_RUN_HOME + "/RenameAppLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResLS", TEST_RUN_HOME + "/RenameAppResLS")
        else:
            assert File.exists(TEST_RUN_HOME + "/ChangeAppLocationLS")

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

        Folder.cleanup("ChangeAppLocationLS")
        Folder.cleanup("ChangeAppLocationAndNameLS")
        Folder.cleanup("ChangeAppResLocationLS")
        Folder.cleanup("ChangeAppResLocationInRootLS")
        Folder.cleanup("RenameAppLS")
        Folder.cleanup("RenameAppResLS")
        Folder.cleanup("ChangeAppLocationLS.app")
        File.remove("ChangeAppLocationLS.ipa")
        Folder.cleanup("ChangeAppLocationAndNameLS.app")
        File.remove("ChangeAppLocationAndNameLS.ipa")
        Folder.cleanup("ChangeAppResLocationLS.app")
        File.remove("ChangeAppResLocationLS.ipa")
        Folder.cleanup("ChangeAppResLocationInRootLS.app")
        File.remove("ChangeAppResLocationInRootLS.ipa")
        Folder.cleanup("RenameAppLS.app")
        File.remove("RenameAppLS.ipa")
        Folder.cleanup("RenameAppResLS.app")
        File.remove("RenameAppResLS.ipa")

    @parameterized.expand([
        ('ChangeAppLocationLS',
         ['new_folder/app/main-view-model.js', 'taps', 'clicks'],
         ['new_folder/app/main-page.xml', 'TAP', 'TEST'],
         ['new_folder/app/app.css', '42', '99']),
        ('ChangeAppLocationAndNameLS',
         ['my folder/my app/main-view-model.js', 'taps', 'clicks'],
         ['my folder/my app/main-page.xml', 'TAP', 'TEST'],
         ['my folder/my app/app.css', '42', '99']),
        ('ChangeAppResLocationLS',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS),
        ('ChangeAppResLocationInRootLS',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS),
        ('RenameAppLS',
         ['renamed_app/main-view-model.js', 'taps', 'clicks'],
         ['renamed_app/main-page.xml', 'TAP', 'TEST'],
         ['renamed_app/app.css', '42', '99']),
        ('RenameAppResLS',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS)
    ])
    def test_001_tns_run_ios_js_css_xml(self, app_name, change_js, change_xml, change_css):
        """Make valid changes in JS,CSS and XML"""

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(app_name, change_js, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(app_name, change_xml, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(app_name, change_css, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml', tolerance=0.26)

        # Rollback all the changes
        ReplaceHelper.rollback(app_name, change_js, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(app_name, change_css, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(app_name, change_xml, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

"""
Test for `tns run android` command on Angular projects with different nsconfig setup.

Run should sync all the changes correctly:
 - Valid changes in CSS, TS, HTML should be applied.
"""

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import EMULATOR_ID, EMULATOR_NAME, CURRENT_OS, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class RunAndroidEmulatorTestsNG(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLSNG"):
            assert "ChangeAppLocationLSNG" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLSNG"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLSNG", TEST_RUN_HOME + "/ChangeAppLocationLSNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLSNG",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameLSNG")
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

    @parameterized.expand([
        ('ChangeAppResLocationLSNG',
         ReplaceHelper.NG_CHANGE_TS,
         ReplaceHelper.NG_CHANGE_HTML,
         ReplaceHelper.NG_CHANGE_CSS),
        ('ChangeAppResLocationInRootLSNG',
         ReplaceHelper.NG_CHANGE_TS,
         ReplaceHelper.NG_CHANGE_HTML,
         ReplaceHelper.NG_CHANGE_CSS),
        ('RenameAppResLSNG',
         ReplaceHelper.NG_CHANGE_TS,
         ReplaceHelper.NG_CHANGE_HTML,
         ReplaceHelper.NG_CHANGE_CSS),
        ('RenameAppLSNG',
         ['renamed_app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter'],
         ['renamed_app/item/items.component.html', '[text]="item.name"', '[text]="item.id"'],
         ['renamed_app/app.css', 'core.light.css', 'core.dark.css']),
        ('ChangeAppLocationLSNG',
         ['new_folder/app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter'],
         ['new_folder/app/item/items.component.html', '[text]="item.name"', '[text]="item.id"'],
         ['new_folder/app/app.css', 'core.light.css', 'core.dark.css']),
        ('ChangeAppLocationAndNameLSNG',
         ['my folder/my app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter'],
         ['my folder/my app/item/items.component.html', '[text]="item.name"', '[text]="item.id"'],
         ['my folder/my app/app.css', 'core.light.css', 'core.dark.css'])
    ])
    def test_001_tns_run_android_ts_css_html(self, app_name, ng_change_ts, ng_change_html, ng_change_css):
        """Make valid changes in JS,CSS and XML"""

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   'Application loaded!',
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=340, check_interval=10)

        # Verify initial state of the app
        assert Device.wait_for_text(device_id=EMULATOR_ID, text="Ter Stegen",
                                    timeout=30), 'Hello-world NG App failed to start or it does not look correct!'

        # Change TS and wait until app is synced
        ReplaceHelper.replace(app_name, ng_change_ts, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application',
                   'Application loaded!',  # This is to verify app is restarted.
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Stegen Ter", timeout=40)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'
        # log_content = File.read(log)
        # assert 'item.service.ts' in log_content, "CLI should transfer TS files!"

        # Clean log (this will not work on windows since file is locked)
        if CURRENT_OS != OSType.WINDOWS:
            File.write(file_path=log, text="")

        # Change HTML and wait until app is synced
        ReplaceHelper.replace(app_name, ng_change_html, sleep=10)

        # Verify app is synced and it is not restarted
        strings = ['items.component.html', 'Successfully synced application', 'Home page loaded!']
        if CURRENT_OS == OSType.WINDOWS:
            not_existing_strings = None  # We can not verify this on windows, because log is not clean
        else:
            not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='9', timeout=30)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Clean log (this will not work on windows since file is locked)
        if CURRENT_OS != OSType.WINDOWS:
            File.write(file_path=log, text="")

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(app_name, ng_change_css, sleep=10)

        # Verify app is synced and it is not restarted
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application', 'Home page loaded!']
        if CURRENT_OS == OSType.WINDOWS:
            not_existing_strings = None  # We can not verify this on windows, because log is not clean
        else:
            not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.

        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='ng-hello-world-home-dark',
                            tolerance=5.0)

        # Revert HTML and wait until app is synced
        ReplaceHelper.rollback(app_name, ng_change_html, sleep=10)

        # Verify app is synced and it is not restarted
        strings = ['items.component.html', 'Successfully synced application', 'Home page loaded!']
        if CURRENT_OS == OSType.WINDOWS:
            not_existing_strings = None  # We can not verify this on windows, because log is not clean
        else:
            not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Stegen Ter", timeout=30)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Revert TS and wait until app is synced
        ReplaceHelper.rollback(app_name, ng_change_ts, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application',
                   'Application loaded!',  # This is to verify app is restarted.
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Ter Stegen", timeout=30)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Revert CSS and wait until app is synced
        ReplaceHelper.rollback(app_name, ng_change_css, sleep=10)
        ReplaceHelper.rollback(app_name, ng_change_css, sleep=10)

        # Verify app is synced and it is not restarted
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application', 'Home page loaded!']
        if CURRENT_OS == OSType.WINDOWS:
            not_existing_strings = None  # We can not verify this on windows, because log is not clean
        else:
            not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=60, not_existing_string_list=not_existing_strings)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='ng-hello-world-home-white', tolerance=5.0)

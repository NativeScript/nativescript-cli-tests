"""
Test for `tns run android` command on Angular projects with different nsconfig setup.

Run should sync all the changes correctly:
 - Valid changes in CSS, TS, HTML should be applied.
"""

import os
from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_PACKAGE, EMULATOR_ID, EMULATOR_NAME, CURRENT_OS
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class RunAndroidEmulatorTestsNG(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()

        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        app_name_change_app_location = "ChangeAppLocation"
        Tns.create_app_ng(app_name=app_name_change_app_location)

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'app')
        app_path = os.path.join(app_name_change_app_location, 'app')
        Folder.cleanup(app_path)
        Folder.copy(src=source, dst=app_path)

        # Change applicationId in app.gradle so that the app can be run successfully
        app_gradle_path = os.path.join('ChangeAppLocation', 'app', 'App_Resources',
                                       'Android', 'app.gradle')
        File.replace(app_gradle_path, "org.nativescript.TestApp", "org.nativescript.ChangeAppLocation")

        # Create the other projects using the initial setup but in different folder
        app_name_change_app_location_and_name = "ChangeAppLocationAndName"
        Folder.cleanup(app_name_change_app_location_and_name)
        Folder.copy(app_name_change_app_location, app_name_change_app_location_and_name)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_location_and_name, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_change_app_location_and_name)
        File.replace(
            os.path.join(app_name_change_app_location_and_name, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_location_and_name)

        app_name_change_app_res_location = "ChangeAppResLocation"
        Folder.cleanup(app_name_change_app_res_location)
        Folder.copy(app_name_change_app_location, app_name_change_app_res_location)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_change_app_res_location)
        File.replace(
            os.path.join(app_name_change_app_res_location, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_res_location)

        app_name_change_app_res_location_in_root = "ChangeAppResLocationInRoot"
        Folder.cleanup(app_name_change_app_res_location_in_root)
        Folder.copy(app_name_change_app_location, app_name_change_app_res_location_in_root)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_change_app_res_location_in_root)
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_res_location_in_root)

        app_name_rename_app = "RenameApp"
        Folder.cleanup(app_name_rename_app)
        Folder.copy(app_name_change_app_location, app_name_rename_app)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_rename_app)
        File.replace(
            os.path.join(app_name_rename_app, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_rename_app)

        app_name_rename_app_res = "RenameAppRes"
        Folder.cleanup(app_name_rename_app_res)
        Folder.copy(app_name_change_app_location, app_name_rename_app_res)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_res, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_rename_app_res)
        File.replace(
            os.path.join(app_name_rename_app_res, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_rename_app_res)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(app_name_change_app_location)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location, 'nsconfig.json', ), app_name_change_app_location)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        Tns.platform_add_android(attributes={"--path": app_name_change_app_location,
                                             "--frameworkPath": ANDROID_PACKAGE})

        # Change app/ name and place to be 'my folder/my app'
        proj_root = os.path.join(app_name_change_app_location_and_name)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_and_name, 'nsconfig.json'),
                  app_name_change_app_location_and_name)
        Folder.create(os.path.join(proj_root, "my folder"))
        os.rename(app_path, os.path.join(proj_root, "my app"))
        Folder.move(os.path.join(proj_root, "my app"), os.path.join(proj_root, "my folder"))
        Tns.platform_add_android(attributes={"--path": app_name_change_app_location_and_name,
                                             "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ location to be 'app/res/App_Resources'
        proj_root = os.path.join(app_name_change_app_res_location)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location, 'nsconfig.json'),
                  app_name_change_app_res_location)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location,
                                             "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root)
        Folder.move(app_res_path, proj_root)
        Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_in_root,
                                             "--frameworkPath": ANDROID_PACKAGE})

        # Change app/ to renamed_app/
        proj_root = os.path.join(app_name_rename_app)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app, 'nsconfig.json'), app_name_rename_app)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        Tns.platform_add_android(attributes={"--path": app_name_rename_app, "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res, 'nsconfig.json'), app_name_rename_app_res)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        Tns.platform_add_android(attributes={"--path": app_name_rename_app_res, "--frameworkPath": ANDROID_PACKAGE})

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

        Folder.cleanup("ChangeAppLocation")
        Folder.cleanup("ChangeAppLocationAndName")
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("ChangeAppResLocationInRoot")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")

    @parameterized.expand([
        ('ChangeAppLocation',
         ['new_folder/app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter'],
         ['new_folder/app/item/items.component.html', '[text]="item.name"', '[text]="item.id"'],
         ['new_folder/app/app.css', 'core.light.css', 'core.dark.css']),
        ('ChangeAppLocationAndName',
         ['my folder/my app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter'],
         ['my folder/my app/item/items.component.html', '[text]="item.name"', '[text]="item.id"'],
         ['my folder/my app/app.css', 'core.light.css', 'core.dark.css']),
        ('ChangeAppResLocation',
         ReplaceHelper.NG_CHANGE_TS,
         ReplaceHelper.NG_CHANGE_HTML,
         ReplaceHelper.NG_CHANGE_CSS),
        ('ChangeAppResLocationInRoot',
         ReplaceHelper.NG_CHANGE_TS,
         ReplaceHelper.NG_CHANGE_HTML,
         ReplaceHelper.NG_CHANGE_CSS),
        ('RenameApp',
         ['renamed_app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter'],
         ['renamed_app/item/items.component.html', '[text]="item.name"', '[text]="item.id"'],
         ['renamed_app/app.css', 'core.light.css', 'core.dark.css']),
        ('RenameAppRes',
         ReplaceHelper.NG_CHANGE_TS,
         ReplaceHelper.NG_CHANGE_HTML,
         ReplaceHelper.NG_CHANGE_CSS)
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
        log_content = File.read(log)
        assert 'item.service.ts' in log_content, "CLI should transfer TS files!"

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

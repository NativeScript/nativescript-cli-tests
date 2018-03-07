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

import os
from parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns


class RunIOSSimulatorTests(BaseClass):
    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Change app/ location to be 'new_folder/app'
        app_name_change_app_location = "ChangeAppLocation"
        Folder.cleanup(app_name_change_app_location)
        Tns.create_app(app_name=app_name_change_app_location,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        proj_root = os.path.join(app_name_change_app_location)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location, 'nsconfig.json', ), app_name_change_app_location)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        Tns.platform_add_ios(attributes={"--path": app_name_change_app_location, "--frameworkPath": IOS_PACKAGE})

        # Change app/ name and place to be 'my folder/my app'
        app_name_change_app_location_and_name = "ChangeAppLocationAndName"
        Folder.cleanup(app_name_change_app_location_and_name)
        Tns.create_app(app_name_change_app_location_and_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        proj_root = os.path.join(app_name_change_app_location_and_name)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_and_name, 'nsconfig.json'),
                  app_name_change_app_location_and_name)
        Folder.create(os.path.join(proj_root, "my folder"))
        os.rename(app_path, os.path.join(proj_root, "my app"))
        Folder.move(os.path.join(proj_root, "my app"), os.path.join(proj_root, "my folder"))
        Tns.platform_add_ios(
            attributes={"--path": app_name_change_app_location_and_name, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ location to be 'app/res/App_Resources'
        app_name_change_app_res_location = "ChangeAppResLocation"
        Folder.cleanup(app_name_change_app_res_location)
        Tns.create_app(app_name=app_name_change_app_res_location,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        proj_root = os.path.join(app_name_change_app_res_location)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location, 'nsconfig.json'),
                  app_name_change_app_res_location)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        Tns.platform_add_ios(attributes={"--path": app_name_change_app_res_location, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ location to be in project root/App_Resources
        app_name_change_app_res_location_in_root = "ChangeAppResLocationInRoot"
        Folder.cleanup(app_name_change_app_res_location_in_root)
        Tns.create_app(app_name_change_app_res_location_in_root,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        proj_root = os.path.join(app_name_change_app_res_location_in_root)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root)
        Folder.move(app_res_path, proj_root)
        Tns.platform_add_ios(
            attributes={"--path": app_name_change_app_res_location_in_root, "--frameworkPath": IOS_PACKAGE})

        # Change app/ to renamed_app/
        app_name_rename_app = "RenameApp"
        Folder.cleanup(app_name_rename_app)
        Tns.create_app(app_name=app_name_rename_app,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        proj_root = os.path.join(app_name_rename_app)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app, 'nsconfig.json'), app_name_rename_app)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        Tns.platform_add_ios(attributes={"--path": app_name_rename_app, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        app_name_rename_app_res = "RenameAppRes"
        Folder.cleanup(app_name_rename_app_res)
        Tns.create_app(app_name=app_name_rename_app_res,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        proj_root = os.path.join(app_name_rename_app_res)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res, 'nsconfig.json'), app_name_rename_app_res)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        Tns.platform_add_ios(attributes={"--path": app_name_rename_app_res, "--frameworkPath": IOS_PACKAGE})

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
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")

    @parameterized.expand([
        ('ChangeAppLocation',
         ['new_folder/app/main-view-model.js', 'taps', 'clicks'],
         ['new_folder/app/main-page.xml', 'TAP', 'TEST'],
         ['new_folder/app/app.css', '42', '99']),
        ('ChangeAppLocationAndName',
         ['my folder/my app/main-view-model.js', 'taps', 'clicks'],
         ['my folder/my app/main-page.xml', 'TAP', 'TEST'],
         ['my folder/my app/app.css', '42', '99']),
        ('ChangeAppResLocation',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS),
        ('ChangeAppResLocationInRoot',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS),
        ('RenameApp',
         ['renamed_app/main-view-model.js', 'taps', 'clicks'],
         ['renamed_app/main-page.xml', 'TAP', 'TEST'],
         ['renamed_app/app.css', '42', '99']),
        ('RenameAppRes',
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
                            expected_image='livesync-hello-world_js_css_xml')

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

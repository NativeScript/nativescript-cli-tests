"""
Tests for `tns debug android` executed on Android Emulator with different nsconfig setup.
"""
import os
from parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.chrome.chrome import Chrome
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import EMULATOR_NAME, EMULATOR_ID, ANDROID_PACKAGE
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class DebugAndroidEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()

        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        app_name_change_app_location = "ChangeAppLocation"
        Folder.cleanup(app_name_change_app_location)
        Tns.create_app(app_name=app_name_change_app_location,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)

        # Rename the app so that all test apps has the same name and reuse the images
        File.replace(
            os.path.join(app_name_change_app_location, 'app', 'App_Resources', 'Android', 'AndroidManifest.xml'),
            "@string/app_name", "TestApp")

        # Create the other projects using the initial setup but in different folder
        app_name_change_app_location_and_name = "ChangeAppLocationAndName"
        Folder.cleanup(app_name_change_app_location_and_name)
        Folder.copy(app_name_change_app_location, app_name_change_app_location_and_name)

        app_name_change_app_res_location = "ChangeAppResLocation"
        Folder.cleanup(app_name_change_app_res_location)
        Folder.copy(app_name_change_app_location, app_name_change_app_res_location)

        app_name_change_app_res_location_in_root = "ChangeAppResLocationInRoot"
        Folder.cleanup(app_name_change_app_res_location_in_root)
        Folder.copy(app_name_change_app_location, app_name_change_app_res_location_in_root)

        app_name_rename_app = "RenameApp"
        Folder.cleanup(app_name_rename_app)
        Folder.copy(app_name_change_app_location, app_name_rename_app)

        app_name_rename_app_res = "RenameAppRes"
        Folder.cleanup(app_name_rename_app_res)
        Folder.copy(app_name_change_app_location, app_name_rename_app_res)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(app_name_change_app_location)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location, 'nsconfig.json', ), app_name_change_app_location)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        Tns.platform_add_android(attributes={"--path": app_name_change_app_location,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_android(attributes={'--path': app_name_change_app_location})

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
        Tns.build_android(attributes={'--path': app_name_change_app_location_and_name})

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
        Tns.build_android(attributes={'--path': app_name_change_app_res_location})

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root)
        Folder.move(app_res_path, proj_root)
        Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_in_root,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_android(attributes={'--path': app_name_change_app_res_location_in_root})

        # Change app/ to renamed_app/s
        proj_root = os.path.join(app_name_rename_app)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app, 'nsconfig.json'), app_name_rename_app)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        Tns.platform_add_android(attributes={"--path": app_name_rename_app, "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_android(attributes={'--path': app_name_rename_app})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res, 'nsconfig.json'), app_name_rename_app_res)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        Tns.platform_add_android(attributes={"--path": app_name_rename_app_res, "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_android(attributes={'--path': app_name_rename_app_res})

    def setUp(self):
        BaseClass.setUp(self)
        Tns.kill()

    def tearDown(self):
        Tns.kill()
        Chrome.stop()
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

    def __verify_debugger_start(self, log):
        strings = [EMULATOR_ID, 'NativeScript Debugger started', 'To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    def __verify_debugger_attach(self, log):
        strings = [EMULATOR_ID, 'To start debugging', 'Chrome', 'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output
        assert "NativeScript Debugger started" not in output

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_001_debug_android(self, app_name):
        """
        Default `tns debug android` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_android(attributes={'--path': app_name, '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_002_debug_android_emulator_debug_brk(self, app_name):
        """
        Starts debugger and stop at the first code statement.
        """

        log = Tns.debug_android(attributes={'--path': app_name, '--debug-brk': '', '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, tolerance=3.0, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_003_debug_android_emulator_start(self, app_name):
        """
        Attach the debug tools to a running app in the Android Emulator
        """

        # Run the app and ensure it works
        Tns.run_android(attributes={'--path': app_name, '--emulator': '', '--justlaunch': ''},
                        assert_success=False, timeout=90)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_android(attributes={'--path': app_name, '--start': '', '--emulator': ''})
        self.__verify_debugger_attach(log=log)

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_100_debug_android_should_start_emulator_if_there_is_no_device(self, app_name):
        """
        Debug android should start emulator if emulator is not running
        """

        Emulator.stop()
        Tns.build_android(attributes={'--path': app_name})
        log = Tns.debug_android(attributes={'--path': app_name, '--emulator': '', '--timeout': '180'})
        strings = ['Starting Android emulator with image']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120)

        # Reset the usage of the predefined emulator in settings.py so the next tests reuse its images
        Emulator.stop()
        Emulator.ensure_available()

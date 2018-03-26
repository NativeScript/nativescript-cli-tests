import os
from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Xcode.cleanup_cache()

        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial setup for all projects
        app_name_change_app_location = "ChangeAppLocation"
        Folder.cleanup(app_name_change_app_location)
        Tns.create_app_ng(app_name=app_name_change_app_location)

        # Create the other projects using the initial setup but in different folder
        app_name_change_app_location_and_name = "ChangeAppLocationAndName"
        Folder.cleanup(app_name_change_app_location_and_name)
        Folder.copy(app_name_change_app_location, app_name_change_app_location_and_name)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_location_and_name, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_change_app_location_and_name)

        app_name_change_app_res_location = "ChangeAppResLocation"
        Folder.cleanup(app_name_change_app_res_location)
        Folder.copy(app_name_change_app_location, app_name_change_app_res_location)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_change_app_res_location)

        app_name_change_app_res_location_in_root = "ChangeAppResLocationInRoot"
        Folder.cleanup(app_name_change_app_res_location_in_root)
        Folder.copy(app_name_change_app_location, app_name_change_app_res_location_in_root)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_change_app_res_location_in_root)

        app_name_rename_app = "RenameApp"
        Folder.cleanup(app_name_rename_app)
        Folder.copy(app_name_change_app_location, app_name_rename_app)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_rename_app)

        app_name_rename_app_res = "RenameAppRes"
        Folder.cleanup(app_name_rename_app_res)
        Folder.copy(app_name_change_app_location, app_name_rename_app_res)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_res, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + app_name_rename_app_res)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(app_name_change_app_location)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location, 'nsconfig.json', ), app_name_change_app_location)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        Tns.platform_add_ios(attributes={"--path": app_name_change_app_location, "--frameworkPath": IOS_PACKAGE})

        # Change app/ name and place to be 'my folder/my app'
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
        proj_root = os.path.join(app_name_change_app_res_location)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location, 'nsconfig.json'),
                  app_name_change_app_res_location)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        Tns.platform_add_ios(attributes={"--path": app_name_change_app_res_location, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root)
        Folder.move(app_res_path, proj_root)
        Tns.platform_add_ios(
            attributes={"--path": app_name_change_app_res_location_in_root, "--frameworkPath": IOS_PACKAGE})

        # Change app/ to renamed_app/
        proj_root = os.path.join(app_name_rename_app)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app, 'nsconfig.json'), app_name_rename_app)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        Tns.platform_add_ios(attributes={"--path": app_name_rename_app, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res, 'nsconfig.json'), app_name_rename_app_res)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        Tns.platform_add_ios(attributes={"--path": app_name_rename_app_res, "--frameworkPath": IOS_PACKAGE})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

        Folder.cleanup("ChangeAppLocation")
        Folder.cleanup("ChangeAppLocationAndName")
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("ChangeAppResLocationInRoot")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_100_build_ios_ng_project(self, app_name):
        Tns.build_ios(attributes={"--path": app_name})

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_200_build_ios_ng_project_release_fordevice(self, app_name):
        Tns.build_ios(attributes={"--path": app_name, "--for-device": "", "--release": ""})
        platform_folder = os.path.join(app_name, 'platforms', 'ios', app_name, 'app', 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"

import os
import unittest

from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TEST_RUN_HOME
from core.tns.tns import Tns


class CreateNSConfigApps(unittest.TestCase):
    app_name_change_app_location = "ChangeAppLocation"
    app_name_change_app_location_and_name = "ChangeAppLocationAndName"
    app_name_change_app_res_location = "ChangeAppResLocation"
    app_name_change_app_res_location_in_root = "ChangeAppResLocationInRoot"
    app_name_rename_app = "RenameApp"
    app_name_rename_app_res = "RenameAppRes"

    app_name_change_app_location_ls = "ChangeAppLocationLS"
    app_name_change_app_location_and_name_ls = "ChangeAppLocationAndNameLS"
    app_name_change_app_res_location_ls = "ChangeAppResLocationLS"
    app_name_change_app_res_location_in_root_ls = "ChangeAppResLocationInRootLS"
    app_name_rename_app_ls = "RenameAppLS"
    app_name_rename_app_res_ls = "RenameAppResLS"

    app_name_change_app_location_ng = "ChangeAppLocationNG"
    app_name_change_app_location_and_name_ng = "ChangeAppLocationAndNameNG"
    app_name_change_app_res_location_ng = "ChangeAppResLocationNG"
    app_name_change_app_res_location_in_root_ng = "ChangeAppResLocationInRootNG"
    app_name_rename_app_ng = "RenameAppNG"
    app_name_rename_app_res_ng = "RenameAppResNG"

    app_name_change_app_location_ls_ng = "ChangeAppLocationLSNG"
    app_name_change_app_location_and_name_ls_ng = "ChangeAppLocationAndNameLSNG"
    app_name_change_app_res_location_ls_ng = "ChangeAppResLocationLSNG"
    app_name_change_app_res_location_in_root_ls_ng = "ChangeAppResLocationInRootLSNG"
    app_name_rename_app_ls_ng = "RenameAppLSNG"
    app_name_rename_app_res_ls_ng = "RenameAppResLSNG"

    errors = 0
    failures = 0

    @classmethod
    def createApps(cls, class_name):

        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        Tns.create_app(cls.app_name_change_app_location)

        # Add release and debug configs
        debug = os.path.join(cls.app_name_change_app_location, 'app', 'config.debug.json')
        release = os.path.join(cls.app_name_change_app_location, 'app', 'config.release.json')
        File.write(file_path=debug, text='{"config":"debug"}')
        File.write(file_path=release, text='{"config":"release"}')

        # Create the other projects using the initial setup but in different folder
        Folder.cleanup(cls.app_name_change_app_location_and_name)
        Folder.copy(cls.app_name_change_app_location, cls.app_name_change_app_location_and_name)

        # Rename the app
        File.replace(
            os.path.join(cls.app_name_change_app_location_and_name, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + cls.app_name_change_app_location_and_name)
        File.replace(
            os.path.join(cls.app_name_change_app_location_and_name, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + cls.app_name_change_app_location_and_name)

        Folder.cleanup(cls.app_name_change_app_res_location)
        Folder.copy(cls.app_name_change_app_location, cls.app_name_change_app_res_location)

        # Rename the app
        File.replace(
            os.path.join(cls.app_name_change_app_res_location, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + cls.app_name_change_app_res_location)
        File.replace(
            os.path.join(cls.app_name_change_app_res_location, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + cls.app_name_change_app_res_location)

        Folder.cleanup(cls.app_name_change_app_res_location_in_root)
        Folder.copy(cls.app_name_change_app_location, cls.app_name_change_app_res_location_in_root)

        # Rename the app
        File.replace(
            os.path.join(cls.app_name_change_app_res_location_in_root, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + cls.app_name_change_app_res_location_in_root)
        File.replace(
            os.path.join(cls.app_name_change_app_res_location_in_root, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + cls.app_name_change_app_res_location_in_root)

        Folder.cleanup(cls.app_name_rename_app)
        Folder.copy(cls.app_name_change_app_location, cls.app_name_rename_app)

        # Rename the app
        File.replace(
            os.path.join(cls.app_name_rename_app, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + cls.app_name_rename_app)
        File.replace(
            os.path.join(cls.app_name_rename_app, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + cls.app_name_rename_app)

        Folder.cleanup(cls.app_name_rename_app_res)
        Folder.copy(cls.app_name_change_app_location, cls.app_name_rename_app_res)

        # Rename the app
        File.replace(
            os.path.join(cls.app_name_rename_app_res, 'package.json'),
            "org.nativescript.ChangeAppLocation", "org.nativescript." + cls.app_name_rename_app_res)
        File.replace(
            os.path.join(cls.app_name_rename_app_res, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + cls.app_name_rename_app_res)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(cls.app_name_change_app_location)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, cls.app_name_change_app_location, 'nsconfig.json', ), cls.app_name_change_app_location)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))

        # Change app/ name and place to be 'my folder/my app'
        proj_root = os.path.join(cls.app_name_change_app_location_and_name)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, cls.app_name_change_app_location_and_name, 'nsconfig.json'),
                  cls.app_name_change_app_location_and_name)
        Folder.create(os.path.join(proj_root, "my folder"))
        os.rename(app_path, os.path.join(proj_root, "my app"))
        Folder.move(os.path.join(proj_root, "my app"), os.path.join(proj_root, "my folder"))

        # Change App_Resources/ location to be 'app/res/App_Resources'
        proj_root = os.path.join(cls.app_name_change_app_res_location)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, cls.app_name_change_app_res_location, 'nsconfig.json'),
                  cls.app_name_change_app_res_location)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(cls.app_name_change_app_res_location_in_root)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, cls.app_name_change_app_res_location_in_root, 'nsconfig.json'),
                  cls.app_name_change_app_res_location_in_root)
        Folder.move(app_res_path, proj_root)
        # Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_res_location_in_root,
        #                                      "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": cls.app_name_change_app_res_location_in_root,
        #                                  "--frameworkPath": IOS_PACKAGE})

        # Change app/ to renamed_app/
        proj_root = os.path.join(cls.app_name_rename_app)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, cls.app_name_rename_app, 'nsconfig.json'), cls.app_name_rename_app)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        # Tns.platform_add_android(attributes={"--path": cls.app_name_rename_app, "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": cls.app_name_rename_app, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(cls.app_name_rename_app_res)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, cls.app_name_rename_app_res, 'nsconfig.json'), cls.app_name_rename_app_res)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        # Tns.platform_add_android(attributes={"--path": cls.app_name_rename_app_res, "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": cls.app_name_rename_app_res, "--frameworkPath": IOS_PACKAGE})

        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location, TEST_RUN_HOME + "/data/Projects/ChangeAppLocation")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_and_name, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndName")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocation")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_in_root, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRoot")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app, TEST_RUN_HOME + "/data/Projects/RenameApp")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_res, TEST_RUN_HOME + "/data/Projects/RenameAppRes")

        Folder.cleanup("ChangeAppLocation")
        Folder.cleanup("ChangeAppLocationAndName")
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("ChangeAppResLocationInRoot")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")
        Folder.cleanup("ChangeAppLocation.app")
        File.remove("ChangeAppLocation.ipa")
        Folder.cleanup("ChangeAppLocationAndName.app")
        File.remove("ChangeAppLocationAndName.ipa")
        Folder.cleanup("ChangeAppResLocation.app")
        File.remove("ChangeAppResLocation.ipa")
        Folder.cleanup("ChangeAppResLocationInRoot.app")
        File.remove("ChangeAppResLocationInRoot.ipa")
        Folder.cleanup("RenameApp.app")
        File.remove("RenameApp.ipa")
        Folder.cleanup("RenameAppRes.app")
        File.remove("RenameAppRes.ipa")
        pass

    @classmethod
    def createAppsLiveSync(cls, class_name):
        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        app_name_change_app_location_ls = "ChangeAppLocationLS"
        Tns.create_app(cls.app_name_change_app_location_ls,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)

        # Rename the app in AndroidManifest.xml to reuse the images
        File.replace(
            os.path.join(cls.app_name_change_app_location_ls, 'app', 'App_Resources', 'Android', 'AndroidManifest.xml'),
            "@string/app_name", "TestApp")

        # Create the other projects using the initial setup but in different folder
        app_name_change_app_location_and_name_ls = "ChangeAppLocationAndNameLS"
        Folder.cleanup(app_name_change_app_location_and_name_ls)
        Folder.copy(app_name_change_app_location_ls, app_name_change_app_location_and_name_ls)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_location_and_name_ls, 'package.json'),
            "org.nativescript.ChangeAppLocationLS", "org.nativescript." + app_name_change_app_location_and_name_ls)
        File.replace(
            os.path.join(app_name_change_app_location_and_name_ls, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_location_and_name_ls)

        app_name_change_app_res_location_ls = "ChangeAppResLocationLS"
        Folder.cleanup(app_name_change_app_res_location_ls)
        Folder.copy(app_name_change_app_location_ls, app_name_change_app_res_location_ls)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_ls, 'package.json'),
            "org.nativescript.ChangeAppLocationLS", "org.nativescript." + app_name_change_app_res_location_ls)
        File.replace(
            os.path.join(app_name_change_app_res_location_ls, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_res_location_ls)

        app_name_change_app_res_location_in_root_ls = "ChangeAppResLocationInRootLS"
        Folder.cleanup(app_name_change_app_res_location_in_root_ls)
        Folder.copy(app_name_change_app_location_ls, app_name_change_app_res_location_in_root_ls)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root_ls, 'package.json'),
            "org.nativescript.ChangeAppLocationLS", "org.nativescript." + app_name_change_app_res_location_in_root_ls)
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root_ls, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_res_location_in_root_ls)

        app_name_rename_app_ls = "RenameAppLS"
        Folder.cleanup(app_name_rename_app_ls)
        Folder.copy(app_name_change_app_location_ls, app_name_rename_app_ls)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_ls, 'package.json'),
            "org.nativescript.ChangeAppLocationLS", "org.nativescript." + app_name_rename_app_ls)
        File.replace(
            os.path.join(app_name_rename_app_ls, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_rename_app_ls)

        app_name_rename_app_res_ls = "RenameAppResLS"
        Folder.cleanup(app_name_rename_app_res_ls)
        Folder.copy(app_name_change_app_location_ls, app_name_rename_app_res_ls)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_res_ls, 'package.json'),
            "org.nativescript.ChangeAppLocationLS", "org.nativescript." + app_name_rename_app_res_ls)
        File.replace(
            os.path.join(app_name_rename_app_res_ls, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_rename_app_res_ls)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(app_name_change_app_location_ls)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_ls, 'nsconfig.json', ), app_name_change_app_location_ls)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_location_ls,
        #                                      "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": app_name_change_app_location_ls, "--frameworkPath": IOS_PACKAGE})

        # Change app/ name and place to be 'my folder/my app'
        proj_root = os.path.join(app_name_change_app_location_and_name_ls)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_and_name_ls, 'nsconfig.json'),
                  app_name_change_app_location_and_name_ls)
        Folder.create(os.path.join(proj_root, "my folder"))
        os.rename(app_path, os.path.join(proj_root, "my app"))
        Folder.move(os.path.join(proj_root, "my app"), os.path.join(proj_root, "my folder"))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_location_and_name_ls,
        #                                      "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(
        #     attributes={"--path": app_name_change_app_location_and_name_ls, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ location to be 'app/res/App_Resources'
        proj_root = os.path.join(app_name_change_app_res_location_ls)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_ls, 'nsconfig.json'),
                  app_name_change_app_res_location_ls)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_ls,
        #                                      "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": app_name_change_app_res_location_ls, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root_ls)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root_ls, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root_ls)
        Folder.move(app_res_path, proj_root)
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_in_root_ls,
        #                                      "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(
        #     attributes={"--path": app_name_change_app_res_location_in_root_ls, "--frameworkPath": IOS_PACKAGE})

        # Change app/ to renamed_app/
        proj_root = os.path.join(app_name_rename_app_ls)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app_ls, 'nsconfig.json'), app_name_rename_app_ls)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        # Tns.platform_add_android(attributes={"--path": app_name_rename_app_ls, "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": app_name_rename_app_ls, "--frameworkPath": IOS_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res_ls)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res_ls, 'nsconfig.json'), app_name_rename_app_res_ls)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        # Tns.platform_add_android(attributes={"--path": app_name_rename_app_res_ls, "--frameworkPath": ANDROID_PACKAGE})
        # Tns.platform_add_ios(attributes={"--path": app_name_rename_app_res_ls, "--frameworkPath": IOS_PACKAGE})

        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_ls, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_and_name_ls, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLS")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_ls, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLS")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_in_root_ls, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLS")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_ls, TEST_RUN_HOME + "/data/Projects/RenameAppLS")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_res_ls, TEST_RUN_HOME + "/data/Projects/RenameAppResLS")

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

    @classmethod
    def createAppsNG(cls, class_name):
        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        app_name_change_app_location_ng = "ChangeAppLocationNG"
        Tns.create_app_ng(app_name=app_name_change_app_location_ng)

        # Create the other projects using the initial setup but in different folder
        app_name_change_app_location_and_name_ng = "ChangeAppLocationAndNameNG"
        Folder.cleanup(app_name_change_app_location_and_name_ng)
        Folder.copy(app_name_change_app_location_ng, app_name_change_app_location_and_name_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_location_and_name_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationNG", "org.nativescript." + app_name_change_app_location_and_name_ng)
        File.replace(
            os.path.join(app_name_change_app_location_and_name_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_location_and_name_ng)

        app_name_change_app_res_location_ng = "ChangeAppResLocationNG"
        Folder.cleanup(app_name_change_app_res_location_ng)
        Folder.copy(app_name_change_app_location_ng, app_name_change_app_res_location_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationNG", "org.nativescript." + app_name_change_app_res_location_ng)
        File.replace(
            os.path.join(app_name_change_app_res_location_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_res_location_ng)

        app_name_change_app_res_location_in_root_ng = "ChangeAppResLocationInRootNG"
        Folder.cleanup(app_name_change_app_res_location_in_root_ng)
        Folder.copy(app_name_change_app_location_ng, app_name_change_app_res_location_in_root_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationNG", "org.nativescript." + app_name_change_app_res_location_in_root_ng)
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_change_app_res_location_in_root_ng)

        app_name_rename_app_ng = "RenameAppNG"
        Folder.cleanup(app_name_rename_app_ng)
        Folder.copy(app_name_change_app_location_ng, app_name_rename_app_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationNG", "org.nativescript." + app_name_rename_app_ng)
        File.replace(
            os.path.join(app_name_rename_app_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_rename_app_ng)

        app_name_rename_app_res_ng = "RenameAppResNG"
        Folder.cleanup(app_name_rename_app_res_ng)
        Folder.copy(app_name_change_app_location_ng, app_name_rename_app_res_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_res_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationNG", "org.nativescript." + app_name_rename_app_res_ng)
        File.replace(
            os.path.join(app_name_rename_app_res_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "__PACKAGE__", "org.nativescript." + app_name_rename_app_res_ng)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(app_name_change_app_location_ng)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_ng, 'nsconfig.json', ), app_name_change_app_location_ng)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_location_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change app/ name and place to be 'my folder/my app'
        proj_root = os.path.join(app_name_change_app_location_and_name_ng)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_and_name_ng, 'nsconfig.json'),
                  app_name_change_app_location_and_name_ng)
        Folder.create(os.path.join(proj_root, "my folder"))
        os.rename(app_path, os.path.join(proj_root, "my app"))
        Folder.move(os.path.join(proj_root, "my app"), os.path.join(proj_root, "my folder"))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_location_and_name_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ location to be 'app/res/App_Resources'
        proj_root = os.path.join(app_name_change_app_res_location_ng)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_ng, 'nsconfig.json'),
                  app_name_change_app_res_location_ng)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root_ng)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root_ng, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root_ng)
        Folder.move(app_res_path, proj_root)
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_in_root_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change app/ to renamed_app/
        proj_root = os.path.join(app_name_rename_app_ng)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app_ng, 'nsconfig.json'), app_name_rename_app_ng)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        # Tns.platform_add_android(attributes={"--path": app_name_rename_app_ng, "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res_ng)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res_ng, 'nsconfig.json'), app_name_rename_app_res_ng)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        # Tns.platform_add_android(attributes={"--path": app_name_rename_app_res_ng, "--frameworkPath": ANDROID_PACKAGE})

        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_and_name_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_in_root_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_ng, TEST_RUN_HOME + "/data/Projects/RenameAppNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_res_ng, TEST_RUN_HOME + "/data/Projects/RenameAppResNG")

        Folder.cleanup("ChangeAppLocationNG")
        Folder.cleanup("ChangeAppLocationAndNameNG")
        Folder.cleanup("ChangeAppResLocationNG")
        Folder.cleanup("ChangeAppResLocationInRootNG")
        Folder.cleanup("RenameAppNG")
        Folder.cleanup("RenameAppResNG")
        Folder.cleanup("ChangeAppLocationNG.app")
        File.remove("ChangeAppLocationNG.ipa")
        Folder.cleanup("ChangeAppLocationAndNameNG.app")
        File.remove("ChangeAppLocationAndNameNG.ipa")
        Folder.cleanup("ChangeAppResLocationNG.app")
        File.remove("ChangeAppResLocationNG.ipa")
        Folder.cleanup("ChangeAppResLocationInRootNG.app")
        File.remove("ChangeAppResLocationInRootNG.ipa")
        Folder.cleanup("RenameAppNG.app")
        File.remove("RenameAppNG.ipa")
        Folder.cleanup("RenameAppResNG.app")
        File.remove("RenameAppResNG.ipa")
        pass

    @classmethod
    def createAppsLiveSyncNG(cls, class_name):
        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        app_name_change_app_location_ls_ng = "ChangeAppLocationLSNG"
        Tns.create_app_ng(app_name=app_name_change_app_location_ls_ng)

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'app')
        app_path = os.path.join(app_name_change_app_location_ls_ng, 'app')
        Folder.cleanup(app_path)
        Folder.copy(src=source, dst=app_path)

        # Change applicationId in app.gradle so that the app can be run successfully
        app_gradle_path = os.path.join('ChangeAppLocationLSNG', 'app', 'App_Resources',
                                       'Android', 'app.gradle')
        File.replace(app_gradle_path, "org.nativescript.TestApp", "org.nativescript.ChangeAppLocationLSNG")

        # Create the other projects using the initial setup but in different folder
        app_name_change_app_location_and_name_ls_ng = "ChangeAppLocationAndNameLSNG"
        Folder.cleanup(app_name_change_app_location_and_name_ls_ng)
        Folder.copy(app_name_change_app_location_ls_ng, app_name_change_app_location_and_name_ls_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_location_and_name_ls_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_change_app_location_and_name_ls_ng)
        File.replace(
            os.path.join(app_name_change_app_location_and_name_ls_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_change_app_location_and_name_ls_ng)

        app_name_change_app_res_location_ls_ng = "ChangeAppResLocationLSNG"
        Folder.cleanup(app_name_change_app_res_location_ls_ng)
        Folder.copy(app_name_change_app_location_ls_ng, app_name_change_app_res_location_ls_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_ls_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_change_app_res_location_ls_ng)
        File.replace(
            os.path.join(app_name_change_app_res_location_ls_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_change_app_res_location_ls_ng)

        app_name_change_app_res_location_in_root_ls_ng = "ChangeAppResLocationInRootLSNG"
        Folder.cleanup(app_name_change_app_res_location_in_root_ls_ng)
        Folder.copy(app_name_change_app_location_ls_ng, app_name_change_app_res_location_in_root_ls_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root_ls_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_change_app_res_location_in_root_ls_ng)
        File.replace(
            os.path.join(app_name_change_app_res_location_in_root_ls_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_change_app_res_location_in_root_ls_ng)

        app_name_rename_app_ls_ng = "RenameAppLSNG"
        Folder.cleanup(app_name_rename_app_ls_ng)
        Folder.copy(app_name_change_app_location_ls_ng, app_name_rename_app_ls_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_ls_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_rename_app_ls_ng)
        File.replace(
            os.path.join(app_name_rename_app_ls_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_rename_app_ls_ng)

        app_name_rename_app_res_ls_ng = "RenameAppResLSNG"
        Folder.cleanup(app_name_rename_app_res_ls_ng)
        Folder.copy(app_name_change_app_location_ls_ng, app_name_rename_app_res_ls_ng)

        # Rename the app
        File.replace(
            os.path.join(app_name_rename_app_res_ls_ng, 'package.json'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_rename_app_res_ls_ng)
        File.replace(
            os.path.join(app_name_rename_app_res_ls_ng, 'app', 'App_Resources', 'Android', 'app.gradle'),
            "org.nativescript.ChangeAppLocationLSNG", "org.nativescript." + app_name_rename_app_res_ls_ng)

        # Change app/ location to be 'new_folder/app'
        proj_root = os.path.join(app_name_change_app_location_ls_ng)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_ls_ng, 'nsconfig.json', ), app_name_change_app_location_ls_ng)
        Folder.create(os.path.join(proj_root, "new_folder"))
        Folder.move(app_path, os.path.join(proj_root, 'new_folder'))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_location_ls_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change app/ name and place to be 'my folder/my app'
        proj_root = os.path.join(app_name_change_app_location_and_name_ls_ng)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_change_app_location_and_name_ls_ng, 'nsconfig.json'),
                  app_name_change_app_location_and_name_ls_ng)
        Folder.create(os.path.join(proj_root, "my folder"))
        os.rename(app_path, os.path.join(proj_root, "my app"))
        Folder.move(os.path.join(proj_root, "my app"), os.path.join(proj_root, "my folder"))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_location_and_name_ls_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ location to be 'app/res/App_Resources'
        proj_root = os.path.join(app_name_change_app_res_location_ls_ng)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_ls_ng, 'nsconfig.json'),
                  app_name_change_app_res_location_ls_ng)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_ls_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root_ls_ng)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root_ls_ng, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root_ls_ng)
        Folder.move(app_res_path, proj_root)
        # Tns.platform_add_android(attributes={"--path": app_name_change_app_res_location_in_root_ls_ng,
        #                                      "--frameworkPath": ANDROID_PACKAGE})

        # Change app/ to renamed_app/
        proj_root = os.path.join(app_name_rename_app_ls_ng)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app_ls_ng, 'nsconfig.json'), app_name_rename_app_ls_ng)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        # Tns.platform_add_android(attributes={"--path": app_name_rename_app_ls_ng, "--frameworkPath": ANDROID_PACKAGE})

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res_ls_ng)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res_ls_ng, 'nsconfig.json'), app_name_rename_app_res_ls_ng)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        # Tns.platform_add_android(attributes={"--path": app_name_rename_app_res_ls_ng, "--frameworkPath": ANDROID_PACKAGE})

        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_ls_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLSNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_location_and_name_ls_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLSNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_ls_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLSNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_change_app_res_location_in_root_ls_ng, TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLSNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_ls_ng, TEST_RUN_HOME + "/data/Projects/RenameAppLSNG")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name_rename_app_res_ls_ng, TEST_RUN_HOME + "/data/Projects/RenameAppResLSNG")

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
        pass

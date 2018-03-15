"""
Test for building projects for iOS platform with different nsconfig setup.
"""
import os
from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, ANDROID_PACKAGE, PROVISIONING, \
    DISTRIBUTION_PROVISIONING, DEVELOPMENT_TEAM
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.xcode.xcode import Xcode


class BuildiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

        base_src = os.path.join(os.getcwd(), 'data', 'nsconfig')

        # Initial create of all projects
        app_name_change_app_location = "ChangeAppLocation"
        Tns.create_app(app_name=app_name_change_app_location)

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
        Tns.platform_add_ios(attributes={"--path": app_name_change_app_location, "--frameworkPath": IOS_PACKAGE})

        Folder.cleanup("ChangeAppLocation.app")
        File.remove("ChangeAppLocation.ipa")

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

        Folder.cleanup("ChangeAppLocationAndName.app")
        File.remove("ChangeAppLocationAndName.ipa")

        # Change App_Resources/ location to be 'app/res/App_Resources'
        proj_root = os.path.join(app_name_change_app_res_location)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location, 'nsconfig.json'),
                  app_name_change_app_res_location)
        Folder.create(os.path.join(app_path, 'res'))
        Folder.move(app_res_path, os.path.join(app_path, 'res'))
        Tns.platform_add_ios(attributes={"--path": app_name_change_app_res_location, "--frameworkPath": IOS_PACKAGE})

        Folder.cleanup("ChangeAppResLocation.app")
        File.remove("ChangeAppResLocation.ipa")

        # Change App_Resources/ location to be in project root/App_Resources
        proj_root = os.path.join(app_name_change_app_res_location_in_root)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_change_app_res_location_in_root, 'nsconfig.json'),
                  app_name_change_app_res_location_in_root)
        Folder.move(app_res_path, proj_root)
        Tns.platform_add_ios(
            attributes={"--path": app_name_change_app_res_location_in_root, "--frameworkPath": IOS_PACKAGE})

        Folder.cleanup("ChangeAppResLocationInRoot.app")
        File.remove("ChangeAppResLocationInRoot.ipa")

        # Change app/ to renamed_app/
        proj_root = os.path.join(app_name_rename_app)
        app_path = os.path.join(proj_root, 'app')

        File.copy(os.path.join(base_src, app_name_rename_app, 'nsconfig.json'), app_name_rename_app)
        os.rename(app_path, os.path.join(proj_root, 'renamed_app'))
        Tns.platform_add_ios(attributes={"--path": app_name_rename_app, "--frameworkPath": IOS_PACKAGE})

        Folder.cleanup("RenameApp.app")
        File.remove("RenameApp.ipa")

        # Change App_Resources/ to My_App_Resources/
        proj_root = os.path.join(app_name_rename_app_res)
        app_path = os.path.join(proj_root, 'app')
        app_res_path = os.path.join(app_path, 'App_Resources')

        File.copy(os.path.join(base_src, app_name_rename_app_res, 'nsconfig.json'), app_name_rename_app_res)
        os.rename(app_res_path, os.path.join(app_path, 'My_App_Resources'))
        Tns.platform_add_ios(attributes={"--path": app_name_rename_app_res, "--frameworkPath": IOS_PACKAGE})

        Folder.cleanup("RenameAppRes.app")
        File.remove("RenameAppRes.ipa")

        Xcode.cleanup_cache()

    def setUp(self):
        BaseClass.setUp(self)
        Simulator.stop()

        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": "ChangeAppLocation"}, assert_success=False)
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": "ChangeAppLocationAndName"},
                            assert_success=False)
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": "ChangeAppResLocation"}, assert_success=False)
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": "ChangeAppResLocation"}, assert_success=False)
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": "RenameApp"}, assert_success=False)
        # Tns.platform_remove(platform=Platform.IOS, attributes={"--path": "RenameAppRes"}, assert_success=False)

    def tearDown(self):
        BaseClass.tearDown(self)
        assert not Simulator.is_running()[0], "Simulator started after " + self._testMethodName

    @classmethod
    def tearDownClass(cls):
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
    def test_001_build_ios(self, app_name):
        Tns.build_ios(attributes={"--path": app_name}, log_trace=True)

        Tns.platform_add_android(attributes={"--path": app_name, "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_ios(attributes={"--path": app_name, "--forDevice": "", "--release": ""}, log_trace=True)

        # Verify no aar and frameworks in platforms folder
        assert not File.pattern_exists(app_name + "/platforms/ios", "*.aar")
        assert not File.pattern_exists(app_name + "/platforms/ios/" + app_name + "/app/tns_modules", "*.framework")

        # Verify ipa has both armv7 and arm64 archs
        run("mv " + app_name + "/platforms/ios/build/device/" + app_name + ".ipa " + app_name + "-ipa.tgz")
        run("unzip -o " + app_name + "-ipa.tgz")
        output = run("lipo -info Payload/" + app_name + ".app/" + app_name)
        Folder.cleanup("Payload")
        assert "Architectures in the fat file: Payload/" + app_name + ".app/" + app_name + " are: armv7 arm64" in output

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_190_build_ios_distribution_provisions(self, app_name):
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": app_name}, assert_success=False)

        # List all provisions and verify them
        output = Tns.build_ios(attributes={"--path": app_name, "--provision": ""}, assert_success=False)
        assert "Provision Name" in output
        assert "Provision UUID" in output
        assert "App Id" in output
        assert "Team" in output
        assert "Type" in output
        assert "Due" in output
        assert "Devices" in output
        assert PROVISIONING in output
        assert DISTRIBUTION_PROVISIONING in output
        assert DEVELOPMENT_TEAM in output

        # Build with correct distribution provision
        build_attributes = {"--path": app_name, "--forDevice": "", "--release": "",
                            "--provision": DISTRIBUTION_PROVISIONING}
        Tns.build_ios(attributes=build_attributes)

        # Verify that passing wrong provision shows user friendly error
        output = Tns.build_ios(attributes={"--path": app_name, "--provision": "fake"}, assert_success=False)
        assert "Failed to find mobile provision with UUID or Name: fake" in output

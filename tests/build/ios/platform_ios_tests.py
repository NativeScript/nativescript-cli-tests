"""
Test platform add (ios)
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, \
    CURRENT_OS, OSType, ANDROID_PACKAGE
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts


class PlatformiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        if CURRENT_OS != OSType.OSX:
            raise NameError("Can not run iOS tests on non OSX OS.")
        Tns.create_app(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)

    def test_102_platform_add_ios(self):
        Tns.platform_add_ios(attributes={"--path": self.app_name})

    def test_200_platform_add_ios_framework_path(self):
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})

        # If project.xcworkspace is there Xcode project name is wrong
        assert not File.exists(self.app_name + "/platforms/ios/TestApp.xcodeproj/project.xcworkspace")

    def test_201_platform_remove_ios(self):
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})
        Tns.platform_remove(platform="ios", attributes={"--path": self.app_name})
        assert Folder.is_empty(self.app_name + '/platforms')
        output = File.read(self.app_name + os.sep + "package.json")
        assert "tns-ios" not in output

    def test_300_platform_add_ios_custom_version(self):
        Tns.platform_add_ios(version="2.1.0", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.1.0\"" in output

    def test_301_platform_update_ios(self):
        Tns.platform_add_ios(version="2.2.0", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.2.0\"" in output

        Tns.platform_update("ios@2.3.0", attributes={"--path": self.app_name, " <  data/keys/enter_key.txt": ""})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.3.0\"" in output

        Tns.build_ios(attributes={"--path": self.app_name})

    def test_310_platform_add_ios_custom_experimental_version(self):
        Tns.platform_add_ios(version="0.9.2-exp-ios-8.2", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"0.9.2-exp-ios-8.2\"" in output

    def test_320_platform_add_ios_custom_bundle_id(self):
        # Create project with different appId
        Folder.cleanup(self.app_name)
        output = Tns.create_app(self.app_name, attributes={"--appid": "org.nativescript.MyApp"}, assert_success=False)
        TnsAsserts.created(self.app_name, output=output, full_check=False)

        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

        # Add iOS platform
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})

        # Verify plist file in native project (after prepare)
        Tns.prepare_ios(attributes={"--path": self.app_name})
        output = File.read(self.app_name + "/platforms/ios/TestApp/TestApp-Info.plist")
        assert "org.nativescript.MyApp" in output

    def test_330_platform_update_ios_platform_not_added(self):
        Tns.create_app(self.app_name)
        output = Tns.platform_update(platform="ios", attributes={"--path": self.app_name}, assert_success=False)
        assert "Platform ios successfully added" in output
        assert not Folder.is_empty(self.app_name + "/platforms/ios/internal/metadata-generator")

    def test_390_LSApplicationQueriesSchemes_merged(self):
        # https: // github.com / NativeScript / nativescript - cli / issues / 3108
        Folder.cleanup(os.path.join(self.app_name, 'app', 'App_Resources', 'iOS', 'Info.plist'))
        info_c = os.path.join('data', 'issues', 'info-plist', 'app', 'Info.plist')
        info_p = os.path.join(self.app_name, 'app', 'App_Resources', 'iOS')
        Folder.copy(info_c, info_p)
        Tns.plugin_add("nativescript-geolocation", attributes={"--path": self.app_name})
        Folder.cleanup(
            os.path.join(self.app_name, 'node_modules', 'nativescript-geolocation', 'platforms', 'ios', 'Info.plist'))
        info_plugin_c = os.path.join('data', 'issues', 'info-plist', 'plugin', 'Info.plist')
        info_plugin_p = os.path.join(self.app_name, 'node_modules', 'nativescript-geolocation', 'platforms', 'ios')
        Folder.copy(info_plugin_c, info_plugin_p)
        Tns.build_ios(attributes={"--path": self.app_name})
        output = File.read(os.path.join(self.app_name, 'platforms', 'ios', 'TestApp', 'TestApp-Info.plist'))
        assert 'itms' in output
        assert "itms-apps" in output
        assert "LSApplicationQueriesSchemes" in output

    def test_391_platform_list(self):
        """Platform list command should list installed platforms and if app is prepared for those platforms"""
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name, update_modules=False)

        # `tns platform list` on brand new project
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.NONE, added=Platform.NONE)

        # `tns platform list` when iOS is added
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.NONE, added=Platform.IOS)

        # `tns platform list` when iOS is prepared
        Tns.prepare_ios(attributes={"--path": self.app_name})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.IOS, added=Platform.IOS)

        # `tns platform list` when android is added (iOS already prepared)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.IOS, added=Platform.BOTH)

        # `tns platform list` when android is prepared (iOS already prepared)
        Tns.prepare_android(attributes={"--path": self.app_name})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.BOTH, added=Platform.BOTH)

        # Verify build both platforms is not allowed
        # Test for https://github.com/NativeScript/nativescript-cli/pull/3425
        output = Tns.run_tns_command(command="build", attributes={"--path": self.app_name})
        assert "The input is not valid sub-command for 'build' command" in output
        assert "<Platform> is the target mobile platform for which you want to build your project" in output

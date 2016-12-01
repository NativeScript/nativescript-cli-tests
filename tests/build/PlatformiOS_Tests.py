"""
Test platform add (ios)
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, IOS_RUNTIME_PATH, \
    CURRENT_OS, OSType
from core.tns.tns import Tns


class PlatformiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        if CURRENT_OS != OSType.OSX:
            raise NameError("Can not run iOS tests on non OSX OS.")

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def test_101_platform_list_ios_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        output = Tns.run_tns_command("platform list", attributes={"--path": self.app_name})
        assert "The project is not prepared for any platform" in output
        assert "Installed platforms:  ios" in output

        Tns.prepare_ios(attributes={"--path": self.app_name})
        output = Tns.run_tns_command("platform list", attributes={"--path": self.app_name})
        assert "The project is prepared for:  ios" in output
        assert "Installed platforms:  ios" in output
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        output = Tns.run_tns_command("platform list", attributes={"--path": self.app_name})
        assert "The project is prepared for:  ios" in output
        assert "Installed platforms:  android" in output

        Tns.prepare_android(attributes={"--path": self.app_name})
        output = Tns.run_tns_command("platform list", attributes={"--path": self.app_name})
        assert "The project is prepared for:  ios and android" in output
        assert "Installed platforms:  android and ios" in output

    def test_102_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name})

    def test_200_platform_add_ios_framework_path(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })

        # If project.xcworkspace is there Xcode project name is wrong
        assert not File.exists(self.app_name + "/platforms/ios/TNSApp.xcodeproj/project.xcworkspace")

    def test_201_platform_remove_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.platform_remove(platform="ios", attributes={"--path": self.app_name})
        assert Folder.is_empty(self.app_name + '/platforms')
        output = File.read(self.app_name + os.sep + "package.json")
        assert "tns-ios" not in output

    def test_202_platform_remove_ios_symlink(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })

        Tns.platform_remove(platform="ios", attributes={"--path": self.app_name})
        assert Folder.is_empty(self.app_name + '/platforms')
        output = File.read(self.app_name + os.sep + "package.json")
        assert "tns-ios" not in output

    def test_300_platform_add_ios_custom_version(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(version="2.1.0", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.1.0\"" in output

    def test_301_platform_update_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(version="2.2.0", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.2.0\"" in output

        Tns.platform_update("ios@2.3.0", attributes={"--path": self.app_name, " <  data/keys/enter_key.txt": ""})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.3.0\"" in output

        Tns.build_ios(attributes={"--path": self.app_name})

    def test_310_platform_add_ios_custom_experimental_version(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(version="0.9.2-exp-ios-8.2", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"0.9.2-exp-ios-8.2\"" in output

    def test_320_platform_add_ios_custom_bundle_id(self):
        # Create project with different appId
        Tns.create_app(self.app_name, attributes={"--appid": "org.nativescript.MyApp"})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

        # Add iOS platform
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })

        # Verify plist file in native project (after prepare)
        Tns.prepare_ios(attributes={"--path": self.app_name})
        output = File.read(self.app_name + "/platforms/ios/TNSApp/TNSApp-Info.plist")
        assert "org.nativescript.MyApp" in output

    def test_330_platform_update_ios_patform_not_added(self):
        Tns.create_app(self.app_name)
        output = Tns.platform_update(platform="ios", attributes={"--path": self.app_name}, assert_success=False)
        assert "Project successfully created." in output
        assert not Folder.is_empty(self.app_name + "/platforms/ios/internal/metadata-generator")

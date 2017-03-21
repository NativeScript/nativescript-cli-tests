"""
Test platform add (ios)
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, \
    CURRENT_OS, OSType, ANDROID_RUNTIME_PATH
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts


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
        output = Tns.create_app(self.app_name, attributes={"--appid": "org.nativescript.MyApp"}, assert_success=False)
        TnsAsserts.created(self.app_name, output=output, full_check=False)

        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

        # Add iOS platform
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        # Verify plist file in native project (after prepare)
        Tns.prepare_ios(attributes={"--path": self.app_name})
        output = File.read(self.app_name + "/platforms/ios/TNSApp/TNSApp-Info.plist")
        assert "org.nativescript.MyApp" in output

    def test_330_platform_update_ios_platform_not_added(self):
        Tns.create_app(self.app_name)
        output = Tns.platform_update(platform="ios", attributes={"--path": self.app_name}, assert_success=False)
        assert successfully_created in output
        assert not Folder.is_empty(self.app_name + "/platforms/ios/internal/metadata-generator")

    def test_390_platform_list(self):
        """Platform list command should list installed platforms and if app is prepared for those platforms"""

        Tns.create_app(self.app_name, update_modules=False)

        # `tns platform list` on brand new project
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.NONE, added=Platform.NONE)

        # `tns platform list` when iOS is added
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.NONE, added=Platform.IOS)

        # `tns platform list` when iOS is prepared
        Tns.prepare_ios(attributes={"--path": self.app_name})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.IOS, added=Platform.IOS)

        # `tns platform list` when android is added (iOS already prepared)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.IOS, added=Platform.BOTH)

        # `tns platform list` when android is prepared (iOS already prepared)
        Tns.prepare_android(attributes={"--path": self.app_name})
        output = Tns.platform_list(attributes={"--path": self.app_name})
        TnsAsserts.platform_list_status(output=output, prepared=Platform.BOTH, added=Platform.BOTH)

"""
Test for building projects with iOS platform
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH, TEST_RUN_HOME
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        super(BuildiOSTests, cls).setUpClass()

        File.remove("TNSApp.app")
        File.remove("TNSApp.ipa")

        Xcode.cleanup_cache()

    def setUp(self):
        BaseClass.setUp(self)

        Folder.cleanup(self.app_name_dash)
        Folder.cleanup(self.app_name_space)
        Folder.cleanup(self.app_name_ios)
        Folder.cleanup(self.app_name_noplatform)
        Folder.cleanup(self.app_name_noplatform + '/platforms/ios/build')

        Folder.cleanup(self.app_name)
        Folder.cleanup(self.app_name_nosym)

    @classmethod
    def tearDownClass(cls):
        File.remove("TNSApp.app")
        File.remove("TNSApp.ipa")

        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_noplatform)
        Folder.cleanup(cls.app_name_dash)
        Folder.cleanup(cls.app_name_space)

    def test_001_build_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "build/emulator/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TNSApp.app")
        assert not File.pattern_exists(self.app_name + "/platforms/ios", "*.aar")
        assert not File.pattern_exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules", "*.framework")

    def test_002_build_ios_release_fordevice(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name,
                                           "--forDevice": "",
                                           "--release": ""
                                           })
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/device/TNSApp.ipa")

        # Verify ipa has both armv7 and arm64 archs
        run("mv " + self.app_name + "/platforms/ios/build/device/TNSApp.ipa TNSApp-ipa.tgz")
        run("tar -xvf TNSApp-ipa.tgz")
        output = run("lipo -info Payload/TNSApp.app/TNSApp")
        assert "armv7" in output
        assert "arm64" in output

    def test_200_build_ios_release(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name,
                                           "--release": ""
                                           })
        assert "CONFIGURATION Release" in output
        assert "build/emulator/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TNSApp.app")

    def test_201_build_ios_fordevice(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name,
                                           "--forDevice": ""
                                           })
        assert "CONFIGURATION Debug" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/device/TNSApp.ipa")

    def test_210_build_ios_non_symlink(self):
        Tns.create_app(self.app_name_nosym)
        Tns.platform_add_ios(attributes={"--path": self.app_name_nosym,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name_nosym,
                                           "--forDevice": "",
                                           "--release": ""
                                           })
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSAppNoSym.app" in output
        assert File.exists(self.app_name_nosym + "/platforms/ios/build/device/TNSAppNoSym.ipa")

    def test_211_build_ios_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        Folder.navigate_to(self.app_name)
        output = Tns.build_ios(tns_path=os.path.join("..", TNS_PATH), attributes={"--path": self.app_name},
                               assert_success=False)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "build/emulator/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TNSApp.app")

    def test_212_build_ios_with_prepare(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        Tns.prepare_ios(attributes={"--path": self.app_name})

        # Even if project is already prepared build will prepare it again
        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "build/emulator/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TNSApp.app")

        # Verify Xcode project name is not empty
        output = File.read(
                self.app_name + "/platforms/ios/TNSApp.xcodeproj/project.xcworkspace/contents.xcworkspacedata")
        assert "__PROJECT_NAME__.xcodeproj" not in output

    def test_213_build_ios_platform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.build_ios(attributes={"--path": self.app_name_noplatform})
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert File.exists(self.app_name_noplatform + "/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_214_build_ios_no_platform_folder(self):
        Tns.create_app(self.app_name_noplatform)
        Folder.cleanup(self.app_name_noplatform + '/platforms')
        output = Tns.build_ios(attributes={"--path": self.app_name_noplatform}, assert_success=False)
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert File.exists(self.app_name_noplatform + "/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_300_build_ios_with_dash(self):
        Tns.create_app(self.app_name_dash)
        Tns.platform_add_ios(attributes={"--path": self.app_name_dash,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        # Verify project builds
        output = Tns.build_ios(attributes={"--path": self.app_name_dash})
        assert "build/emulator/tnsapp.app" in output
        assert File.exists(self.app_name_dash + "/platforms/ios/build/emulator/tnsapp.app")

        # Verify project id
        output = File.read(self.app_name_dash + os.sep + "package.json")
        assert "org.nativescript.tnsapp" in output

    def test_301_build_ios_with_space(self):
        Tns.create_app(self.app_name_space)
        Tns.platform_add_ios(attributes={"--path": "\"" + self.app_name_space + "\"",
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        # Verify project builds
        output = Tns.build_ios(attributes={"--path": "\"" + self.app_name_space + "\""})
        assert "build/emulator/tnsapp.app" in output
        assert File.exists(self.app_name_space + "/platforms/ios/build/emulator/TNSApp.app")

    def test_302_build_ios_with_ios_in_path(self):
        Tns.create_app(self.app_name_ios)
        Tns.platform_add_ios(attributes={"--path": self.app_name_ios,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        # Verify project builds
        output = Tns.build_ios(attributes={"--path": self.app_name_ios})
        assert "build/emulator/myiosapp.app" in output
        assert File.exists(self.app_name_ios + "/platforms/ios/build/emulator/myiosapp.app")
        assert File.exists(self.app_name_ios + "/platforms/ios/myiosapp/myiosapp-Prefix.pch")

    def test_310_build_ios_with_copy_to(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name, "--copy-to": "./"})
        assert "build/emulator/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TNSApp.app")
        assert File.exists("TNSApp.app")

    def test_311_build_ios_release_with_copy_to(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.build_ios(attributes={"--path": self.app_name,
                                           "--forDevice": "",
                                           "--release": "",
                                           "--copy-to": "./"
                                           })
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/device/TNSApp.ipa")
        assert File.exists("TNSApp.ipa")

    def test_400_build_ios_with_wrong_param(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.build_ios(attributes={"--path": self.app_name_noplatform, "--wrongParam": ""},
                               assert_success=False)
        assert "The option 'wrongParam' is not supported." in output
        assert "error" not in output

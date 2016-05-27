"""
Test for building projects with iOS platform
"""
import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        File.remove("TNSApp.app")
        File.remove("TNSApp.ipa")

        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNSAppNoSym')

        Xcode.cleanup_cache()

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./tns-app')
        Folder.cleanup('./tns app')
        Folder.cleanup('./my-ios-app')
        Folder.cleanup('./TNS_AppNoPlatform')
        Folder.cleanup('TNS_AppNoPlatform/platforms/ios/build')

        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNSAppNoSym')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        File.remove("TNSApp.app")
        File.remove("TNSApp.ipa")

        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNS_AppNoPlatform')
        Folder.cleanup('./tns-app')
        Folder.cleanup('./tns app')

    def test_001_build_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(TNS_PATH + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

        assert not File.pattern_exists("TNS_App/platforms/ios", "*.aar")
        assert not File.pattern_exists("TNS_App/platforms/ios/TNSApp/app/tns_modules", "*.framework")

    def test_002_build_ios_release_fordevice(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(
                TNS_PATH +
                " build ios --path TNS_App --forDevice --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")

        # Verify ipa has both armv7 and arm64 archs
        run("mv TNS_App/platforms/ios/build/device/TNSApp.ipa TNSApp-ipa.tgz")
        run("tar -xvf TNSApp-ipa.tgz")
        output = run("lipo -info Payload/TNSApp.app/TNSApp")
        assert "armv7" in output
        assert "arm64" in output

    def test_200_build_ios_release(self):
        Tns.create_app_platform_add(app_name="TNS_App",
                                    platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH,
                                    symlink=True)
        output = run(TNS_PATH + " build ios --path TNS_App --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_201_build_ios_fordevice(self):
        Tns.create_app_platform_add(app_name="TNS_App",
                                    platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH,
                                    symlink=True)
        output = run(TNS_PATH + " build ios --path TNS_App --forDevice")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")

    def test_210_build_ios_non_symlink(self):
        Tns.create_app_platform_add(
                app_name="TNSAppNoSym",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH)
        output = run(
                TNS_PATH +
                " build ios --path TNSAppNoSym --forDevice --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSAppNoSym.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists(
                "TNSAppNoSym/platforms/ios/build/device/TNSAppNoSym.ipa")

    def test_211_build_ios_inside_project(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(
                os.path.join(
                        "..",
                        TNS_PATH) +
                " build ios --path TNS_App")
        os.chdir(current_dir)

        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_212_build_ios_wiht_prepare(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        Tns.prepare(path="TNS_App", platform="ios")

        output = run(TNS_PATH + " build ios --path TNS_App")

        # Even if project is already prepared build will prepare it again
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

        # Verify Xcode project name is not empty
        output = run("cat TNS_App/platforms/ios/TNSApp.xcodeproj/" +
                     "project.xcworkspace/contents.xcworkspacedata")
        assert "__PROJECT_NAME__.xcodeproj" not in output

    def test_213_build_ios_platform_not_added(self):
        Tns.create_app(app_name="TNS_AppNoPlatform")
        output = run(TNS_PATH + " build ios --path TNS_AppNoPlatform")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists(
                "TNS_AppNoPlatform/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_214_build_ios_no_platform_folder(self):
        Tns.create_app(app_name="TNS_AppNoPlatform")
        Folder.cleanup('./TNS_AppNoPlatform/platforms')
        output = run(TNS_PATH + " build ios --path TNS_AppNoPlatform")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists(
                "TNS_AppNoPlatform/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_300_build_ios_with_dash(self):
        Tns.create_app_platform_add(
                app_name="tns-app",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        # Verify project builds
        output = run(TNS_PATH + " build ios --path tns-app")
        assert "Project successfully prepared" in output
        assert "build/emulator/tnsapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("tns-app/platforms/ios/build/emulator/tnsapp.app")

        # Verify project id
        output = run("cat tns-app/package.json")
        assert "org.nativescript.tnsapp" in output

    def test_301_build_ios_with_space(self):
        Tns.create_app_platform_add(
                app_name="\"tns app\"",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        # Verify project builds
        output = run(TNS_PATH + " build ios --path \"tns app\"")
        assert "Project successfully prepared" in output
        assert "build/emulator/tnsapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("tns app/platforms/ios/build/emulator/tnsapp.app")

    def test_302_build_ios_with_ios_in_path(self):
        Tns.create_app_platform_add(
                app_name="my-ios-app",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        # Verify project builds
        output = run(TNS_PATH + " build ios --path my-ios-app")
        assert "Project successfully prepared" in output
        assert "build/emulator/myiosapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists(
                "my-ios-app/platforms/ios/build/emulator/myiosapp.app")
        assert File.exists(
                "my-ios-app/platforms/ios/myiosapp/myiosapp-Prefix.pch")

    def test_310_build_ios_with_copy_to(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(TNS_PATH + " build ios --path TNS_App --copy-to ./")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")
        assert File.exists("TNSApp.app")

    def test_311_build_ios_release_with_copy_to(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(
                TNS_PATH +
                " build ios --path TNS_App --forDevice --release --copy-to ./")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")
        assert File.exists("TNSApp.ipa")

    def test_400_build_ios_with_wrong_param(self):
        Tns.create_app(app_name="TNS_AppNoPlatform")
        output = run(
                TNS_PATH +
                " build iOS --debug --path TNS_AppNoPlatform")
        assert "The option 'debug' is not supported." in output
        assert "error" not in output

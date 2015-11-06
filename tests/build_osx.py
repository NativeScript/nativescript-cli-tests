'''
Test for building projects with iOS platform
'''
import os
import unittest

from helpers._os_lib import cleanup_folder, remove, run_aut, file_exists
from helpers._tns_lib import TNSPATH, create_project, prepare, \
    create_project_add_platform, IOS_RUNTIME_SYMLINK_PATH

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# W1401 - Anomalous backslash in string: "%s"
# pylint: disable=C0103, C0111, R0201, R0904, W1401
class BuildiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        remove("TNSApp.app")
        remove("TNSApp.ipa")

        cleanup_folder('./TNS_App')
        cleanup_folder('./TNSAppNoSym')

        # create_project_add_platform(proj_name="TNS_App", \
        #                            platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
        #                            symlink=True)
        # create_project_add_platform(proj_name="TNSAppNoSym", \
        #                            platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH)

        # Delete derived data
        run_aut("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        # Delete precompiled headers
        run_aut('sudo find /var/folders/ -name \'*tnsapp-*\' -exec rm -rf {} \;')

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./tns-app')
        cleanup_folder('./tns app')
        cleanup_folder('./my-ios-app')
        cleanup_folder('./TNS_AppNoPlatform')
        cleanup_folder('TNS_AppNoPlatform/platforms/ios/build')

        cleanup_folder('./TNS_App')
        cleanup_folder('./TNSAppNoSym')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        remove("TNSApp.app")
        remove("TNSApp.ipa")

        cleanup_folder('./TNS_App')
        cleanup_folder('./TNS_AppNoPlatform')
        cleanup_folder('./tns-app')
        cleanup_folder('./tns app')

    def test_001_build_ios(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(TNSPATH + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_002_build_ios_release_fordevice(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(
            TNSPATH +
            " build ios --path TNS_App --forDevice --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")

        # Verify ipa has both armv7 and arm64 archs
        output = run_aut(
            "mv TNS_App/platforms/ios/build/device/TNSApp.ipa TNSApp-ipa.tgz")
        output = run_aut("tar -xvf TNSApp-ipa.tgz")
        output = run_aut("lipo -info Payload/TNSApp.app/TNSApp")
        assert "armv7" in output
        assert "arm64" in output

    def test_200_build_ios_release(self):
        create_project_add_platform(proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(TNSPATH + " build ios --path TNS_App --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_201_build_ios_fordevice(self):
        create_project_add_platform(proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(TNSPATH + " build ios --path TNS_App --forDevice")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")

    def test_210_build_ios_non_symlink(self):
        create_project_add_platform(
            proj_name="TNSAppNoSym",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH)
        output = run_aut(
            TNSPATH +
            " build ios --path TNSAppNoSym --forDevice --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSAppNoSym.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists(
            "TNSAppNoSym/platforms/ios/build/device/TNSAppNoSym.ipa")

    def test_211_build_ios_inside_project(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(
            os.path.join(
                "..",
                TNSPATH) +
            " build ios --path TNS_App")
        os.chdir(current_dir)

        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_212_build_ios_wiht_prepare(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        prepare(path="TNS_App", platform="ios")

        output = run_aut(TNSPATH + " build ios --path TNS_App")

        # Even if project is already prepared build will prepare it again
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

        # Verify Xcode project name is not empty
        output = run_aut("cat TNS_App/platforms/ios/TNSApp.xcodeproj/" + \
                         "project.xcworkspace/contents.xcworkspacedata")
        assert not "__PROJECT_NAME__.xcodeproj" in output

    def test_213_build_ios_platform_not_added(self):
        create_project(proj_name="TNS_AppNoPlatform")
        output = run_aut(TNSPATH + " build ios --path TNS_AppNoPlatform")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists(
            "TNS_AppNoPlatform/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_214_build_ios_no_platform_folder(self):
        create_project(proj_name="TNS_AppNoPlatform")
        cleanup_folder('./TNS_AppNoPlatform/platforms')
        output = run_aut(TNSPATH + " build ios --path TNS_AppNoPlatform")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists(
            "TNS_AppNoPlatform/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_300_build_ios_with_dash(self):
        create_project_add_platform(
            proj_name="tns-app",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        # Verify project builds
        output = run_aut(TNSPATH + " build ios --path tns-app")
        assert "Project successfully prepared" in output
        assert "build/emulator/tnsapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("tns-app/platforms/ios/build/emulator/tnsapp.app")

        # Verify project id
        output = run_aut("cat tns-app/package.json")
        assert "org.nativescript.tnsapp" in output

    def test_301_build_ios_with_space(self):
        create_project_add_platform(
            proj_name="\"tns app\"",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        # Verify project builds
        output = run_aut(TNSPATH + " build ios --path \"tns app\"")
        assert "Project successfully prepared" in output
        assert "build/emulator/tnsapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("tns app/platforms/ios/build/emulator/tnsapp.app")

    def test_302_build_ios_with_ios_in_path(self):
        create_project_add_platform(
            proj_name="my-ios-app",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        # Verify project builds
        output = run_aut(TNSPATH + " build ios --path my-ios-app")
        assert "Project successfully prepared" in output
        assert "build/emulator/myiosapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists(
            "my-ios-app/platforms/ios/build/emulator/myiosapp.app")
        assert file_exists(
            "my-ios-app/platforms/ios/myiosapp/myiosapp-Prefix.pch")

    def test_310_build_ios_with_copy_to(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(TNSPATH + " build ios --path TNS_App --copy-to ./")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")
        assert file_exists("TNSApp.app")

    def test_311_build_ios_release_with_copy_to(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(
            TNSPATH +
            " build ios --path TNS_App --forDevice --release --copy-to ./")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")
        assert file_exists("TNSApp.ipa")

    def test_400_build_ios_with_wrong_param(self):
        create_project(proj_name="TNS_AppNoPlatform")
        output = run_aut(
            TNSPATH +
            " build iOS --debug --path TNS_AppNoPlatform")
        assert "The option 'debug' is not supported." in output
        assert not "error" in output

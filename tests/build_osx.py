'''
Test for building projects with iOS platform
'''
import os
import unittest

from helpers._os_lib import CleanupFolder, remove, runAUT, FileExists
from helpers._tns_lib import tnsPath, CreateProject, Prepare, \
    CreateProjectAndAddPlatform, iosRuntimeSymlinkPath

# pylint: disable=R0201, C0111


class BuildiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        remove("TNSApp.app")
        remove("TNSApp.ipa")

        CleanupFolder('./TNS_App')
        CleanupFolder('./TNSAppNoSym')
        # CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        # CreateProjectAndAddPlatform(projName="TNSAppNoSym", platform="ios", frameworkPath=iosRuntimeSymlinkPath)
        # Delete derived data
        runAUT("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        # Delete precompiled headers
        runAUT("sudo find /var/folders/ -name '*tnsapp-*' -exec rm -rf {} \;")

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./tns-app')
        CleanupFolder('./tns app')
        CleanupFolder('./my-ios-app')
        CleanupFolder('./TNS_AppNoPlatform')
        CleanupFolder('TNS_AppNoPlatform/platforms/ios/build')

        CleanupFolder('./TNS_App')
        CleanupFolder('./TNSAppNoSym')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        remove("TNSApp.app")
        remove("TNSApp.ipa")

        CleanupFolder('./TNS_App')
        CleanupFolder('./TNS_AppNoPlatform')
        CleanupFolder('./tns-app')
        CleanupFolder('./tns app')

    def test_001_Build_iOS(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_002_Build_iOS_Release(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(tnsPath + " build ios --path TNS_App --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_003_Build_iOS_ForDevice(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(tnsPath + " build ios --path TNS_App --forDevice")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/device/TNSApp.ipa")

    def test_004_Build_iOS_Release_ForDevice(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(
            tnsPath +
            " build ios --path TNS_App --forDevice --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/device/TNSApp.ipa")

        # Verify ipa has both armv7 and arm64 archs
        output = runAUT(
            "mv TNS_App/platforms/ios/build/device/TNSApp.ipa TNSApp-ipa.tgz")
        output = runAUT("tar -xvf TNSApp-ipa.tgz")
        output = runAUT("lipo -info Payload/TNSApp.app/TNSApp")
        assert "armv7" in output
        assert "arm64" in output

    def test_200_Build_iOS_None_SymlinkProject(self):
        CreateProjectAndAddPlatform(
            projName="TNSAppNoSym",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath)
        output = runAUT(
            tnsPath +
            " build ios --path TNSAppNoSym --forDevice --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSAppNoSym.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists(
            "TNSAppNoSym/platforms/ios/build/device/TNSAppNoSym.ipa")

    def test_201_Build_iOS_InsideProject(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(
            os.path.join(
                "..",
                tnsPath) +
            " build ios --path TNS_App")
        os.chdir(currentDir)

        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_202_Build_iOS_WithPrepare(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        Prepare(path="TNS_App", platform="ios")

        output = runAUT(tnsPath + " build ios --path TNS_App")

        # Even if project is already prepared build will prepare it again
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

        # Verify Xcode project name is not empty
        command = "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.xcworkspace/contents.xcworkspacedata"
        output = runAUT(command)
        assert not "__PROJECT_NAME__.xcodeproj" in output

    def test_210_Build_iOS_PlatformNotAdded(self):
        CreateProject(projName="TNS_AppNoPlatform")
        output = runAUT(tnsPath + " build ios --path TNS_AppNoPlatform")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists(
            "TNS_AppNoPlatform/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_211_Build_iOS_NoPlatformsFolder(self):
        CreateProject(projName="TNS_AppNoPlatform")
        CleanupFolder('./TNS_AppNoPlatform/platforms')
        output = runAUT(tnsPath + " build ios --path TNS_AppNoPlatform")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSAppNoPlatform.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists(
            "TNS_AppNoPlatform/platforms/ios/build/emulator/TNSAppNoPlatform.app")

    def test_300_Build_iOS_WithDashInPath(self):
        CreateProjectAndAddPlatform(
            projName="tns-app",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        # Verify project builds
        output = runAUT(tnsPath + " build ios --path tns-app")
        assert "Project successfully prepared" in output
        assert "build/emulator/tnsapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("tns-app/platforms/ios/build/emulator/tnsapp.app")

        # Verify project id
        output = runAUT("cat tns-app/package.json")
        assert "org.nativescript.tnsapp" in output

    def test_301_Build_iOS_WithSpaceInPath(self):
        CreateProjectAndAddPlatform(
            projName="\"tns app\"",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        # Verify project builds
        output = runAUT(tnsPath + " build ios --path \"tns app\"")
        assert "Project successfully prepared" in output
        assert "build/emulator/tnsapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("tns app/platforms/ios/build/emulator/tnsapp.app")

    def test_302_Build_iOS_WithiOSinPath(self):
        CreateProjectAndAddPlatform(
            projName="my-ios-app",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        # Verify project builds
        output = runAUT(tnsPath + " build ios --path my-ios-app")
        assert "Project successfully prepared" in output
        assert "build/emulator/myiosapp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists(
            "my-ios-app/platforms/ios/build/emulator/myiosapp.app")
        assert FileExists(
            "my-ios-app/platforms/ios/myiosapp/myiosapp-Prefix.pch")

    def test_310_Build_iOS_With_CopyTo(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(tnsPath + " build ios --path TNS_App --copy-to ./")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNSApp.app")
        assert FileExists("TNSApp.app")

    def test_311_Build_iOS_Release_With_CopyTo(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(
            tnsPath +
            " build ios --path TNS_App --forDevice --release --copy-to ./")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert FileExists("TNS_App/platforms/ios/build/device/TNSApp.ipa")
        assert FileExists("TNSApp.ipa")

    def test_401_Build_iOS_WithWrongParam(self):
        CreateProject(projName="TNS_AppNoPlatform")
        output = runAUT(
            tnsPath +
            " build iOS --debug --path TNS_AppNoPlatform")
        assert "The option 'debug' is not supported." in output
        assert not "error" in output

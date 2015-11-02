'''
Test for building projects with Android platform
'''
import os
import platform
import unittest

from helpers._os_lib import CleanupFolder, remove, runAUT, FileExists
from helpers._tns_lib import tnsPath, CreateProject, CreateProjectAndAddPlatform, \
    androidRuntimePath, Prepare, androidKeyStorePath, androidKeyStorePassword, \
    androidKeyStoreAlias, androidKeyStoreAliasPassword, PlatformAdd, \
    androidRuntimeSymlinkPath

# pylint: disable=R0201, C0111
class Build_Linux(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        remove("TNSApp-debug.apk")
        remove("TNSApp-release.apk")

        CleanupFolder('./TNS_App')
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./tns-app');
        CleanupFolder('./TNSAppNoPlatform')
        CleanupFolder('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        remove("TNSApp-debug.apk")
        remove("TNSApp-release.apk")

        CleanupFolder('./TNS_App')
        CleanupFolder('./TNSAppNoPlatform')
        CleanupFolder('./TNS_AppSymlink')

    def test_001_Build_Android(self):
        output = runAUT(tnsPath + " build android --path TNS_App")
        assert ("Project successfully prepared" in output)

        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)

        assert not ("ERROR" in output)
        assert not ("FAILURE" in output)

        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_002_Build_Android_Release(self):
        output = runAUT(tnsPath + " build android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App")

        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)

        assert ("Project successfully built" in output)
        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")

    def test_003_Build_SymlinkProject(self):
        if ('Windows' in platform.platform()):
            print "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282"
        else:
            CreateProject(projName="TNS_AppSymlink")
            output = PlatformAdd(platform="android", path="TNS_AppSymlink", frameworkPath=androidRuntimeSymlinkPath, symlink=True)
            assert("Project successfully created" in output)
            output = runAUT(tnsPath + " build android --path TNS_AppSymlink")
            assert ("Project successfully prepared" in output)
            assert ("BUILD SUCCESSFUL" in output)
            assert ("Project successfully built" in output)

            # Verify build does not modify original manifest
            runAUT("cat " + androidRuntimeSymlinkPath + "/framework/src/main/AndroidManifest.xml")
            assert ("__PACKAGE__" in output, "Build modify original AndroidManifest.xml, this is a problem!")
            assert ("__APILEVEL__" in output, "Build modify original AndroidManifest.xml, this is a problem!")

    def test_200_Build_Android_InsideProject(self):
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " build android --path TNS_App")
        os.chdir(currentDir);
        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)
        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_201_Build_Android_WithPrepare(self):

        Prepare(path="TNS_App", platform="android")
        output = runAUT(tnsPath + " build android --path TNS_App")

        # Even if project is already prepared build will prepare it again
        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)
        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_210_Build_Android_PlatformNotAdded(self):
        CreateProject(projName="TNSAppNoPlatform")
        output = runAUT(tnsPath + " build android --path TNSAppNoPlatform --log trace")

        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)

        assert not ("ERROR" in output)
        assert not ("FAILURE" in output)
        assert FileExists("TNSAppNoPlatform/platforms/android/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_211_Build_Android_NoPlatformsFolder(self):
        CreateProject(projName="TNSAppNoPlatform")
        CleanupFolder('./TNSAppNoPlatform/platforms')
        output = runAUT(tnsPath + " build android --path TNSAppNoPlatform  --log trace")

        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)

        assert not ("ERROR" in output)
        assert not ("FAILURE" in output)
        assert FileExists("TNSAppNoPlatform/platforms/android/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_300_Build_Android_WithAdditionalStylesXML(self):

        # This is test for issue 644

        runAUT("mkdir -p TestApp/app/App_Resources/Android/values")
        runAUT("cp testdata/data/styles.xml TestApp/app/App_Resources/Android/values")
        output = runAUT(tnsPath + " build android --path TNS_App")

        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)
        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_301_Build_Android_WithDashInPath(self):
        CreateProjectAndAddPlatform(projName="tns-app", platform="android", frameworkPath=androidRuntimePath)

        # Verify project builds
        output = runAUT(tnsPath + " build android --path tns-app")
        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)
        assert FileExists("tns-app/platforms/android/build/outputs/apk/tnsapp-debug.apk")

        # Verify project id
        output = runAUT("cat tns-app/package.json")
        assert ("org.nativescript.tnsapp" in output)

        # Verify AndroidManifest.xml
        output = runAUT("cat tns-app/platforms/android/src/main/AndroidManifest.xml")
        assert ("org.nativescript.tnsapp" in output)

    def test_302_Build_Android_WithGZFiles(self):

        # Skip on Windows, because tar is not available
        if ('Windows' not in platform.platform()):
            runAUT("tar -czf TNS_App/app/app.tar.gz TNS_App/app/app.js")
            assert(FileExists("TNS_App/app/app.tar.gz"))

        output = runAUT(tnsPath + " build android --path TNS_App")

        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)

    def test_303_Build_Android_Sdk22(self):

        output = runAUT(tnsPath + " build android --compileSdk 22 --path TNS_App")
        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)
        assert not ("ERROR" in output)
        assert not ("FAILURE" in output)

        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_304_Build_Android_Sdk23(self):

        output = runAUT(tnsPath + " build android --compileSdk 23 --path TNS_App")
        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)
        assert not ("ERROR" in output)
        assert not ("FAILURE" in output)

        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_305_Build_Android_Sdk19(self):

        output = runAUT(tnsPath + " build android --compileSdk 19 --path TNS_App --log trace")
        assert ("Project successfully prepared" in output)
        assert ("BUILD FAILED" in output)

    def test_306_Build_Android_Sdk99(self):

        output = runAUT(tnsPath + " build android --compileSdk 99 --path TNS_App")
        assert ("Project successfully prepared" in output)
        assert ("You have specified '99' for compile sdk, but it is not installed on your system." in output)

    def test_310_Build_Android_Release_With_CopyTo(self):
        output = runAUT(tnsPath + " build android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App --copy-to ./")

        assert ("Project successfully prepared" in output)
        assert ("BUILD SUCCESSFUL" in output)

        assert ("Project successfully built" in output)
        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")
        assert FileExists("TNSApp-release.apk")

    def test_311_Build_Android_With_CopyTo(self):
        output = runAUT(tnsPath + " build android --path TNS_App --copy-to ./")
        assert ("Project successfully prepared" in output)

        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)

        assert not ("ERROR" in output)
        assert not ("FAILURE" in output)

        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert FileExists("TNSApp-debug.apk")

    def test_400_Build_MissingPlatform(self):
        output = runAUT(tnsPath + " build")
        assert ("The input is not valid sub-command for 'build' command" in output)
        assert ("# build" in output)

        if 'Darwin' in platform.platform():
            assert ("$ tns build <Platform>" in output)
        else:
            assert ("$ tns build android" in output)

    def test_401_Build_InvalidPlatform(self):
        output = runAUT(tnsPath + " build invalidCommand")
        assert ("The input is not valid sub-command for 'build' command" in output)

    def test_402_Build_Android_WithOutPath(self):
        output = runAUT(tnsPath + " build android")
        assert ("No project found at or above" in output)
        assert ("and neither was a --path specified." in output)

    def test_403_Build_Android_WithInvalidPath(self):
        output = runAUT(tnsPath + " build android --path invalidPath")
        assert ("No project found at or above" in output)
        assert ("and neither was a --path specified." in output)

    def test_404_Build_Android_WithWrongParam(self):
        output = runAUT(tnsPath + " build android --invalidOption --path TNS_App")
        assert ("The option 'invalidOption' is not supported" in output)

    def test_405_Build_IOSonNotOSXMachine(self):
        output = runAUT(tnsPath + " build ios --path TNS_App")
        if 'Darwin' in platform.platform():
            pass
        else:
            assert ("Applications for platform ios can not be built on this OS" in output)

    def test_410_Build_Android_Release_NoKeyWarn(self):
        output = runAUT(tnsPath + " build android --release --path TNS_App")

        assert ("When producing a release build, you need to specify all --key-store-* options." in output)
        assert ("# build android" in output)
        assert not FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")

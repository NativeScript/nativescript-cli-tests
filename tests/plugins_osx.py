import os
import platform
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimePath, \
    tnsPath, CreateProject, androidRuntimePath, PlatformAdd, Build, \
    iosRuntimeSymlinkPath, androidRuntimeSymlinkPath

# pylint: disable=R0201, C0111
class Plugins_OSX(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        runAUT("rm -rf ~/Library/Developer/Xcode/DerivedData/*")  # Delete derived data
        CleanupFolder('./TNS_App');

    def tearDown(self):
        CleanupFolder('./TNS_App');

    def test_001_PluginAdd_Before_PlatformAdd_iOS(self):
        CreateProject(projName="TNS_App");
        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_PluginAdd_After_PlatformAdd_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App");
        assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_201_PluginAdd_Before_PlatformAdd_iOS(self):
        CreateProject(projName="TNS_App");
        output = runAUT(tnsPath + " plugin add nativescript-telerik-ui --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert FileExists("TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert FileExists("TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert FileExists("TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        PlatformAdd(platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True, path="TNS_App")
        Build(platform="ios", path="TNS_App")

    def test_202_PluginAdd_After_PlatformAdd_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        output = runAUT(tnsPath + " plugin add nativescript-telerik-ui --path TNS_App");
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert FileExists("TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert FileExists("TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert FileExists("TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Build(platform="ios", path="TNS_App")

    def test_203_PluginAdd_InsideProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(currentDir);
        assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_204_BuildAppWithPluginInsideProject(self):

        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)

        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(currentDir);
        assert "Successfully installed plugin tns-plugin" in output

        output = runAUT(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

    def test_300_BuildAppWithPluginOutside(self):

        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)

        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        output = runAUT(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

    def test_301_BuildAppForBothPlatforms(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        PlatformAdd(platform="android", frameworkPath=androidRuntimeSymlinkPath, path="TNS_App", symlink=True)

        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        # Verify files of the plugin
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        assert FileExists("TNS_App/node_modules/tns-plugin/test.android.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/test.ios.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/test2.android.xml")
        assert FileExists("TNS_App/node_modules/tns-plugin/test2.ios.xml")

        output = runAUT(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

        output = runAUT(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output

        assert FileExists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify platform specific files
        assert FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.js")
        assert FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.xml")
        assert not FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.ios.js")
        assert not FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.android.js")
        assert not FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.android.xml")

        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.js")
        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.xml")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.ios.js")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.android.js")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.android.xml")

    def test_302_PlugingAndNPMModulesInSameProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)

        output = runAUT(tnsPath + " plugin add nativescript-social-share --path TNS_App")
        assert "Successfully installed plugin nativescript-social-share" in output

        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT("npm install nativescript-appversion --save")
        os.chdir(currentDir);
        assert not "ERR!" in output
        assert "nativescript-appversion@" in output

        output = runAUT(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        # Verify plugin and npm module files
        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/package.json")
        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/social-share.js")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/social-share.android.js")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/social-share.ios.js")

        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/package.json")
        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/appversion.js")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/appversion.android.js")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/appversion.ios.js")

    def test_401_PluginAdd_InvalidPlugin(self):
        CreateProject(projName="TNS_App");
        output = runAUT(tnsPath + " plugin add wd --path TNS_App")
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file contains a nativescript key and try again" in output

    def test_403_PluginAdd_PluginNotSupportedOnSpecificPlatform(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        PlatformAdd(platform="android", frameworkPath=androidRuntimeSymlinkPath, path="TNS_App", symlink=True)

        output = runAUT(tnsPath + " plugin add tns-plugin@1.0.2 --path TNS_App")
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output

import os
import platform
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import create_project_add_platform, androidRuntimePath, \
    tnsPath, create_project, platform_add, Build

# pylint: disable=R0201, C0111


class Plugins_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_PluginAdd_Before_platform_add_Android(self):
        create_project(proj_name="TNS_App")
        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_PluginAdd_After_platform_add_Android(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_003_PluginAdd_InsideProject(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(current_dir)
        if 'Windows' not in platform.platform():
            assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_100_BuildAppWithPluginAddedInsideProject(self):

        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = runAUT(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output

        # Not valid for 1.3.0+
        # assert "Creating TNSApp-debug-unaligned.apk and signing it with a debug key..." in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output
        assert not "FAILURE" in output

        assert FileExists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert FileExists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

    def test_200_PluginAdd_Before_platform_add_Android(self):
        create_project(proj_name="TNS_App")
        output = runAUT(
            tnsPath +
            " plugin add nativescript-telerik-ui --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert FileExists(
            "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert FileExists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert FileExists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        platform_add(
            platform="android",
            framework_path=androidRuntimePath,
            path="TNS_App")
        Build(platform="android", path="TNS_App")

    def test_201_PluginAdd_After_platform_add_Android(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        output = runAUT(
            tnsPath +
            " plugin add nativescript-telerik-ui --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert FileExists(
            "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert FileExists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert FileExists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Build(platform="android", path="TNS_App")

    def test_300_BuildAppWithPluginAddedOutsideProject(self):

        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)

        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        output = runAUT(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output

        # Not valid for 1.3.0+
        # assert "Creating TNSApp-debug-unaligned.apk and signing it with a debug key..." in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output
        assert not "FAILURE" in output
        assert FileExists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert FileExists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

    @unittest.skip("This test breaks the xml parser.")
    def test_400_PluginAdd_NotExistingPlugin(self):
        create_project(proj_name="TNS_App")
        output = runAUT(tnsPath + " plugin add fakePlugin --path TNS_App")
        assert "no such package available" in output

    def test_401_PluginAdd_InvalidPlugin(self):
        create_project(proj_name="TNS_App")
        output = runAUT(tnsPath + " plugin add wd --path TNS_App")
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file contains a nativescript key and try again" in output

    def test_403_PluginAdd_PluginNotSupportedOnSpecificPlatform(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        output = runAUT(
            tnsPath +
            " plugin add tns-plugin@1.0.2 --path TNS_App")
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output

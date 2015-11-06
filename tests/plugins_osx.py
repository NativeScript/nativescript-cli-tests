import os
import platform
import unittest

from helpers._os_lib import cleanup_folder, run_aut, file_exists
from helpers._tns_lib import create_project_add_platform, iosRuntimePath, \
    tnsPath, create_project, androidRuntimePath, platform_add, build, \
    iosRuntimeSymlinkPath, androidRuntimeSymlinkPath

# pylint: disable=R0201, C0111


class Plugins_OSX(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        run_aut("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        cleanup_folder('./TNS_App')

    def tearDown(self):
        cleanup_folder('./TNS_App')

    def test_001_PluginAdd_Before_platform_add_iOS(self):
        create_project(proj_name="TNS_App")
        output = run_aut(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert file_exists("TNS_App/node_modules/tns-plugin/index.js")
        assert file_exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_PluginAdd_After_platform_add_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)
        output = run_aut(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert file_exists("TNS_App/node_modules/tns-plugin/index.js")
        assert file_exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_201_PluginAdd_Before_platform_add_iOS(self):
        create_project(proj_name="TNS_App")
        output = run_aut(
            tnsPath +
            " plugin add nativescript-telerik-ui --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert file_exists(
            "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert file_exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert file_exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        platform_add(
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True,
            path="TNS_App")
        build(platform="ios", path="TNS_App")

    def test_202_PluginAdd_After_platform_add_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)
        output = run_aut(
            tnsPath +
            " plugin add nativescript-telerik-ui --path TNS_App")
        if 'Windows' not in platform.platform():
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert file_exists(
            "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert file_exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert file_exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        build(platform="ios", path="TNS_App")

    def test_203_PluginAdd_InsideProject(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimePath)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert file_exists("TNS_App/node_modules/tns-plugin/index.js")
        assert file_exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_204_BuildAppWithPluginInsideProject(self):

        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = run_aut(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

    def test_300_BuildAppWithPluginOutside(self):

        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        output = run_aut(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        output = run_aut(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

    def test_301_BuildAppForBothPlatforms(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)
        platform_add(
            platform="android",
            framework_path=androidRuntimeSymlinkPath,
            path="TNS_App",
            symlink=True)

        output = run_aut(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        # Verify files of the plugin
        assert file_exists("TNS_App/node_modules/tns-plugin/index.js")
        assert file_exists("TNS_App/node_modules/tns-plugin/package.json")
        assert file_exists("TNS_App/node_modules/tns-plugin/test.android.js")
        assert file_exists("TNS_App/node_modules/tns-plugin/test.ios.js")
        assert file_exists("TNS_App/node_modules/tns-plugin/test2.android.xml")
        assert file_exists("TNS_App/node_modules/tns-plugin/test2.ios.xml")

        output = run_aut(tnsPath + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

        output = run_aut(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output

        assert file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify platform specific files
        assert file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.js")
        assert file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.xml")
        assert not file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.ios.js")
        assert not file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.android.js")
        assert not file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.android.xml")

        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.js")
        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.xml")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.ios.js")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.android.js")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.android.xml")

    def test_302_PlugingAndNPMModulesInSameProject(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)

        output = run_aut(
            tnsPath +
            " plugin add nativescript-social-share --path TNS_App")
        assert "Successfully installed plugin nativescript-social-share" in output

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut("npm install nativescript-appversion --save")
        os.chdir(current_dir)
        assert not "ERR!" in output
        assert "nativescript-appversion@" in output

        output = run_aut(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        # Verify plugin and npm module files
        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/package.json")
        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/social-share.js")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/social-share.android.js")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-social-share/social-share.ios.js")

        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/package.json")
        assert file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/appversion.js")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/appversion.android.js")
        assert not file_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-appversion/appversion.ios.js")

    def test_401_PluginAdd_InvalidPlugin(self):
        create_project(proj_name="TNS_App")
        output = run_aut(tnsPath + " plugin add wd --path TNS_App")
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file contains a nativescript key and try again" in output

    def test_403_PluginAdd_PluginNotSupportedOnSpecificPlatform(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)
        platform_add(
            platform="android",
            framework_path=androidRuntimeSymlinkPath,
            path="TNS_App",
            symlink=True)

        output = run_aut(
            tnsPath +
            " plugin add tns-plugin@1.0.2 --path TNS_App")
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output

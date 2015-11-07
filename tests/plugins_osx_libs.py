'''
Test for plugin* commands in context of iOS
'''
import unittest

from helpers._os_lib import cleanup_folder, run_aut, file_exists
from helpers._tns_lib import build, IOS_RUNTIME_SYMLINK_PATH, \
    TNSPATH, create_project, platform_add, prepare, create_project_add_platform

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class Plugins_OSX_Libs(unittest.TestCase):

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
        pass

    def test_201_plugin_add_StaticLib_Universal_Before_platform_add_ios(self):
        create_project(proj_name="TNS_App")

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/static-lib/hello-plugin --path TNS_App")
        assert "TNS_App/node_modules/hello" in output
        assert "Successfully installed plugin hello." in output
        assert file_exists("TNS_App/node_modules/hello/package.json")
        assert file_exists("TNS_App/node_modules/hello/hello-plugin.ios.js")
        assert file_exists(
            "TNS_App/node_modules/hello/platforms/ios/HelloLib.a")
        assert file_exists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert file_exists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")

        output = run_aut("cat TNS_App/package.json")
        assert "static-lib/hello-plugin" in output

        platform_add(
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            path="TNS_App",
            symlink=True)
        output = build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" not in output
        assert file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/package.json")
        assert file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/hello-plugin.js")
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_202_plugin_add_StaticLib_Universal_After_platform_add_ios(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/static-lib/hello-plugin --path TNS_App")
        assert "TNS_App/node_modules/hello" in output
        assert "Successfully installed plugin hello." in output
        assert file_exists("TNS_App/node_modules/hello/package.json")
        assert file_exists("TNS_App/node_modules/hello/hello-plugin.ios.js")
        assert file_exists(
            "TNS_App/node_modules/hello/platforms/ios/HelloLib.a")
        assert file_exists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert file_exists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")

        output = run_aut("cat TNS_App/package.json")
        assert "static-lib/hello-plugin" in output

        output = build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" not in output
        assert file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/package.json")
        assert file_exists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/hello-plugin.js")
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_401_plugin_add_StaticLib_NonUniversal(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/static-lib/bye-plugin --path TNS_App")
        assert "TNS_App/node_modules/bye" in output

        output = prepare(platform="ios", path="TNS_App", assert_success=False)
        assert "The static library at" in output
        assert "ByeLib.a is not built for one or more of the following required architectures:" in output
        assert "armv7, arm64, i386." in output
        assert "The static library must be built for all required architectures." in output

import unittest

from helpers._os_lib import cleanup_folder, run_aut, file_exists
from helpers._tns_lib import IOS_RUNTIME_SYMLINK_PATH, \
    TNSPATH, prepare, create_project_add_platform

# pylint: disable=R0201, C0111


class Plugins_OSX_Sandbox_Pods(unittest.TestCase):

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

    def test_001_PluginAdd_Sandbox_Pod_CanWriteInAppFolder(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/nativescript-ios-working-with-sandbox-plugin --path TNS_App")
        assert "Successfully installed plugin nativescript-ios-working-with-sandbox-plugin." in output

        output = run_aut("cat TNS_App/package.json")
        assert "nativescript-ios-working-with-sandbox-plugin" in output

        output = prepare(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin nativescript-ios-working-with-sandbox-plugin for ios." in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp/app/I_MADE_THIS_FILE.txt")
        assert "content" in output

    def test_401_PluginAdd_Sandbox_Pod_CanNotWriteOutsideAppFolder(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/nativescript-ios-fail-with-sandbox-plugin --path TNS_App")
        assert "Successfully installed plugin nativescript-ios-fail-with-sandbox-plugin." in output

        output = run_aut("cat TNS_App/package.json")
        assert "nativescript-ios-fail-with-sandbox-plugin" in output

        output = prepare(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin nativescript-ios-fail-with-sandbox-plugin for ios." in output

        assert "sh: ../I_MADE_THIS_FILE.txt: Operation not permitted" in output
        assert not file_exists("TNS_App/platforms/I_MADE_THIS_FILE.txt")

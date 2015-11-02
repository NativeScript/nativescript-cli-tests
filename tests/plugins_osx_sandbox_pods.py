import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import iosRuntimeSymlinkPath, \
    tnsPath, Prepare, CreateProjectAndAddPlatform


class Plugins_OSX_Sandbox_Pods(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        runAUT("rm -rf ~/Library/Developer/Xcode/DerivedData/*")  # Delete derived data
        CleanupFolder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_PluginAdd_Sandbox_Pod_CanWriteInAppFolder(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)

        output = runAUT(tnsPath + " plugin add QA-TestApps/CocoaPods/nativescript-ios-working-with-sandbox-plugin --path TNS_App")
        assert ("Successfully installed plugin nativescript-ios-working-with-sandbox-plugin." in output)

        output = runAUT("cat TNS_App/package.json")
        assert ("nativescript-ios-working-with-sandbox-plugin" in output)

        output = Prepare(platform="ios", path="TNS_App")
        assert ("Successfully prepared plugin nativescript-ios-working-with-sandbox-plugin for ios." in output)

        output = runAUT("cat TNS_App/platforms/ios/TNSApp/app/I_MADE_THIS_FILE.txt")
        assert ("content" in output)

    def test_401_PluginAdd_Sandbox_Pod_CanNotWriteOutsideAppFolder(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)

        output = runAUT(tnsPath + " plugin add QA-TestApps/CocoaPods/nativescript-ios-fail-with-sandbox-plugin --path TNS_App")
        assert ("Successfully installed plugin nativescript-ios-fail-with-sandbox-plugin." in output)

        output = runAUT("cat TNS_App/package.json")
        assert ("nativescript-ios-fail-with-sandbox-plugin" in output)

        output = Prepare(platform="ios", path="TNS_App")
        assert ("Successfully prepared plugin nativescript-ios-fail-with-sandbox-plugin for ios." in output)

        assert ("sh: ../I_MADE_THIS_FILE.txt: Operation not permitted" in output)
        assert not FileExists("TNS_App/platforms/I_MADE_THIS_FILE.txt")

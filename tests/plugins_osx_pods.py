import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import Build, iosRuntimePath, \
    tnsPath, CreateProject, PlatformAdd, Prepare

class Plugins_OSX_Pods(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App');

    def tearDown(self):
        CleanupFolder('./TNS_App');

    def test_001_PluginAdd_Pod_GoogleMaps_Before_PlatformAdd_iOS(self):
        CreateProject(projName="TNS_App");

        output = runAUT(tnsPath + " plugin add QA-TestApps/CocoaPods/googlesdk --path TNS_App")
        assert ("TNS_App/node_modules/googlesdk" in output)
        assert ("Successfully installed plugin googlesdk." in output)
        assert FileExists("TNS_App/node_modules/googlesdk/package.json")
        assert FileExists("TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("dependencies" in output)
        assert ("googlesdk" in output)

        PlatformAdd(platform="ios", frameworkPath=iosRuntimePath, path="TNS_App")
        output = Prepare(platform="ios", path="TNS_App")
        assert ("Installing pods..." in output)
        assert ("Successfully prepared plugin googlesdk for ios." in output)

        output = runAUT("cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedatas")
        assert ("location = \"group:TNSApp.xcodeproj\">" in output)
        assert ("location = \"group:Pods/Pods.xcodeproj\">" in output)

        assert FileExists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")
        Build(platform="ios", path="TNS_App")

    def test_002_PluginAdd_Pod_GoogleMaps_After_PlatformAdd_iOS(self):
        CreateProject(projName="TNS_App");
        PlatformAdd(platform="ios", frameworkPath=iosRuntimePath, path="TNS_App")

        output = runAUT(tnsPath + " plugin add QA-TestApps/CocoaPods/googlesdk --path TNS_App")
        assert ("TNS_App/node_modules/googlesdk" in output)
        assert ("Successfully installed plugin googlesdk." in output)
        assert FileExists("TNS_App/node_modules/googlesdk/package.json")
        assert FileExists("TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("dependencies" in output)
        assert ("googlesdk" in output)

        output = runAUT("cat TNS_App/platforms/ios/Podfile")
        assert ("source 'https://github.com/CocoaPods/Specs.git'" in output)
        assert ("platform :ios, '8.1'" in output)
        assert ("pod 'GoogleMaps'" in output)

        output = Build(platform="ios", path="TNS_App")
        assert ("Installing pods..." in output)
        assert ("Successfully prepared plugin googlesdk for ios." in output)

        output = runAUT("cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedatas")
        assert ("location = \"group:TNSApp.xcodeproj\">" in output)
        assert ("location = \"group:Pods/Pods.xcodeproj\">" in output)

        assert FileExists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")


#     def test_401_PluginAdd_InvalidPod(self):
#         pass
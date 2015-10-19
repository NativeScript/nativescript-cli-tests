import unittest
import shutil

from helpers._os_lib import CleanupFolder, replace, catAppFile, uninstall_app
from helpers._tns_lib import iosRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRealDeviceRunning, \
    StopEmulators, StopSimulators

class LiveSync_iOS(unittest.TestCase):

    # LiveSync Tests on iOS Device

    @classmethod
    def setUpClass(cls):
        GivenRealDeviceRunning(platform="ios")
        StopEmulators()
        StopSimulators()
        uninstall_app("TNSApp", platform="ios", fail=False)
        CleanupFolder('./TNS_App');
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath) 
        Run(platform="ios", path="TNS_App")
        
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        uninstall_app("TNSApp", platform="ios", fail=False)

    def test_001_LiveSync_iOS_XmlJsCss_Files(self):

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")
        LiveSync(platform="ios", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("ios", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
        output = catAppFile("ios", "TNSApp", "app/app.css")
        assert ("font-size: 20;" in output)

    def test_002_LiveSync_iOS_Device_XmlFile(self):

        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="ios", device="54dec253cfb494a373ca281e12b2b0fc4912aec1", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
 
    @unittest.skip("TODO: Fix this test.")
    def test_004_LiveSync_iOS_Watch(self):
        pass

    def test_011_LiveSync_iOS_TnsModules_Files(self):

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace("TNS_App/node_modules/tns-core-modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")
        LiveSync(platform="ios", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)
        output = catAppFile("ios", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    def test_021_LiveSync_iOS_AddNewFiles(self):

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")
        LiveSync(platform="ios", path="TNS_App")
 
        output = catAppFile("ios", "TNSApp", "app/test.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("ios", "TNSApp", "app/test.js")
        assert ("page.bindingContext = vmModule.mainViewModel;" in output)
        output = catAppFile("ios", "TNSApp", "app/test.css")
        assert ("color: #284848;" in output)
 
    @unittest.skip("Not implemented.")
    def test_031_LiveSync_iOS_DeleteFiles(self):
        pass
 
    def test_301_LiveSync_MultiplePlatforms(self):

        output = LiveSync(path="TNS_App", assertSuccess=False)
        assert ("Multiple device platforms detected (iOS and Android). Specify platform or device on command line" in output)

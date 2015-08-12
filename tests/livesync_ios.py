import unittest
import os, psutil, shutil, subprocess, time

from helpers._os_lib import CleanupFolder, replace, catAppFile, uninstall_app
from helpers._tns_lib import iosRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRealDeviceRunning

class LiveSync_iOS(unittest.TestCase):

    # LiveSync Tests on Android Emulator

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App');
        GivenRealDeviceRunning(platform="ios")
        uninstall_app("TNSApp")

    def tearDown(self):
        pass

    def test_001_LiveSync_iOS_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="ios", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_002_LiveSync_iOS_Device_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")

        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        # a0036be7bace11a09a86fd5a31fca9c8c105011f
        LiveSync(platform="ios", device="e3b6171ff676e093d0c8dcb0aefea1e63ca5c825", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
 
    @unittest.skip("TODO: Fix this test.")
    def test_004_LiveSync_iOS_Watch(self):
        pass
 
    def test_011_LiveSync_iOS_JsFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")
 
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="ios", path="TNS_App")
 
        output = catAppFile("ios", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
 
    def test_012_LiveSync_iOS_CssFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")
 
        replace("TNS_App/app/app.css", "30", "20")
        LiveSync(platform="ios", path="TNS_App")
 
        output = catAppFile("ios", "TNSApp", "app/app.css")
        assert ("font-size: 20;" in output)
 
    def test_013_LiveSync_iOS_TnsModules_File(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")
 
        replace("TNS_App/app/tns_modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")
        LiveSync(platform="ios", path="TNS_App")
 
        output = catAppFile("ios", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)
 
    def test_014_LiveSync_iOS_TnsModules_LICENSE(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")
 
        replace("TNS_App/app/tns_modules/LICENSE", "2015", "9999")
        LiveSync(platform="ios", path="TNS_App")
 
        output = catAppFile("ios", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)
 
    def test_021_LiveSync_iOS_AddNewFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")
 
        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")
        LiveSync(platform="ios", path="TNS_App")
 
        output = catAppFile("ios", "TNSApp", "app/test.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("ios", "TNSApp", "app/test.js")
        assert ("page.bindingContext = vmModule.mainViewModel;" in output)
        output = catAppFile("ios", "TNSApp", "app/test.css")
        assert ("color: #284848;" in output)
 
    @unittest.skip("Not implemented.")
    def test_031_LiveSync_iOS_DeleteFiles(self):
        pass
 
    def test_301_LiveSync_MultiplePlatforms(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        output = LiveSync(path="TNS_App", assertSuccess=False)
        assert ("Multiple device platforms detected (iOS and Android). Specify platform or device on command line." in output)

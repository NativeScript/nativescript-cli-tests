import os, shutil, time
import unittest

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRealDeviceRunning, \
    StopEmulators, StopSimulators, GetPhysicalDeviceId

class LiveSync_Android(unittest.TestCase):

    # LiveSync Tests on Android Device

    @classmethod
    def setUpClass(cls):

        StopEmulators()
        StopSimulators()

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')
        GivenRealDeviceRunning(platform="android")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_001_LiveSync_Android_XmlJsCss_TnsModules_Files(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace("TNS_App/node_modules/tns-core-modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")

        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
        output = catAppFile("android", "TNSApp", "app/app.css")
        assert ("font-size: 20;" in output)

        output = catAppFile("android", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)
        output = catAppFile("android", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    # This test executes the Run -> LiveSync -> Run work flow on an android device with API level 21. 
    def test_002_LiveSync_Android_Device_XmlFile_Run(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        deviceId = GetPhysicalDeviceId(platform="android")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", device=deviceId, path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

        replace("TNS_App/app/main-page.xml", "TEST", "RUN")
        Run(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"RUN\" tap=\"{{ tapAction }}\" />" in output)

    def test_201_LiveSync_Android_AddNewFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile("TNS_App/app/main-view-model.js", "TNS_App/app/test/main-view-model.js")

        LiveSync(platform="android", path="TNS_App")
        time.sleep(5)
                
        output = catAppFile("android", "TNSApp", "app/test.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("android", "TNSApp", "app/test.js")
        assert ("page.bindingContext = vmModule.mainViewModel;" in output)
        output = catAppFile("android", "TNSApp", "app/test.css")
        assert ("color: #284848;" in output)
        output = catAppFile("android", "TNSApp", "app/test/main-view-model.js")
        assert ("HelloWorldModel.prototype.tapAction" in output)

    @unittest.skip("TODO: Not implemented.")
    def test_202_LiveSync_Android_DeleteFiles(self):
        pass

    @unittest.skip("TODO: Implement this test.")
    def test_203_LiveSync_Android_Watch(self):
        pass

    def test_301_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        output = LiveSync(path="TNS_App", assertSuccess=False)

        assert ("Multiple device platforms detected (iOS and Android). Specify platform or device on command line" in output)

    @unittest.skip("TODO: Implement this test..")
    def test_302_LiveSync_Android_MultipleDevice(self):
        pass

    # TODO:
    # - test to detect a deleted file
    # - test to check change in a file that is not being used will not affect the app
    # - test to check JavaScript, XML and CSS do not crash the app

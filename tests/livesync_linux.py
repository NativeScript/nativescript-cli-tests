import os, psutil, shutil, subprocess, time
from platform import platform
import unittest

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRunningEmulator, \
    StopEmulators, StopSimulators, GetDeviceCount


class LiveSync_Linux(unittest.TestCase):

    # LiveSync Tests on Android Emulator

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
        GivenRunningEmulator()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        StopEmulators()

    def test_001_LiveSync_Android_XmlJsCss_Files(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
        output = catAppFile("android", "TNSApp", "app/app.css")
        assert ("font-size: 20;" in output)

    def test_002_LiveSync_Android_Device_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", device="emulator-5554", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_003_LiveSync_Android_Emulator_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", emulator=True, path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    @unittest.skip("TODO: Fix this test.")
    def test_004_LiveSync_Android_Watch(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")

        print "tns livesync android --watch --path TNS_App"
        pr = subprocess.Popen("tns livesync android --watch --path TNS_App", shell=True)
        pr_pid = pr.pid

        time.sleep(60)
        print "assert"
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output)

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")

        time.sleep(15)
        print "assert"
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output)

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")

        time.sleep(15)
        print "assert"
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output)

        print "killing child ..."
        pr.terminate()

        time.sleep(5)
        if psutil.pid_exists(pr_pid):
            print "force killing child ..."
            pr.kill()

    def test_011_LiveSync_Android_TnsModules_Files(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace("TNS_App/node_modules/tns-core-modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)

        output = catAppFile("android", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    def test_021_LiveSync_Android_AddNewFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")
        LiveSync(platform="android", path="TNS_App")

        time.sleep(1)
        output = catAppFile("android", "TNSApp", "app/test.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("android", "TNSApp", "app/test.js")
        assert ("page.bindingContext = vmModule.mainViewModel;" in output)
        output = catAppFile("android", "TNSApp", "app/test.css")
        assert ("color: #284848;" in output)

    @unittest.skip("Not implemented.")
    def test_031_LiveSync_Android_DeleteFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        # .xml
        # .js
        # .css
        os.remove("TNS_App/app/LICENSE")
        LiveSync(platform="android", path="TNS_App")

        # .xml
        # .js
        # .css
        output = catAppFile("android", "TNSApp", "app/LICENSE")
        assert ("cat: files/app/LICENSE: No such file or directory" in output)

    def test_301_LiveSync_Android_Emulator_SpecifyDevice_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", emulator=True, device="emulator-5554", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_302_LiveSync_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(path="TNS_App", platform="android")
        time.sleep(5)

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_303_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        LiveSync(path="TNS_App", platform="android")

        time.sleep(3)
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)
        
    def test_304_LiveSync_PlatformNotSpecified_XmlFile(self):
        
        # This test is not valid if simulator or real iOS device is avalable
        if GetDeviceCount(platform="ios") == 0:
            CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
            Run(platform="android", path="TNS_App")

            replace("TNS_App/app/main-page.xml", "TAP", "TEST")
            LiveSync(path="TNS_App")
            time.sleep(5)

            output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

import os, psutil, shutil, subprocess, time
import unittest

from helpers._os_lib import CleanupFolder, replace, catAppFileOnEmulator
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRunningEmulator, \
    StopEmulators, StopSimulators


class LiveSync_Linux(unittest.TestCase):

    # LiveSync Tests on Android Emulator
    # TODO: Add tests for #942

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

    def test_001_LiveSync_Android_XmlJsCss_TnsModules_Files(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", device="emulator-5554", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace("TNS_App/node_modules/tns-core-modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")

        LiveSync(platform="android", emulator=True, device="emulator-5554", path="TNS_App")

        output = catAppFileOnEmulator("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFileOnEmulator("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
        output = catAppFileOnEmulator("android", "TNSApp", "app/app.css")
        assert ("font-size: 20;" in output)

        output = catAppFileOnEmulator("android", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)
        output = catAppFileOnEmulator("android", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    def test_201_LiveSync_Android_AddNewFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", device="emulator-5554", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile("TNS_App/app/main-view-model.js", "TNS_App/app/test/main-view-model.js")
        LiveSync(platform="android", device="emulator-5554", path="TNS_App")

        time.sleep(1)
        output = catAppFileOnEmulator("android", "TNSApp", "app/test.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFileOnEmulator("android", "TNSApp", "app/test.js")
        assert ("page.bindingContext = vmModule.mainViewModel;" in output)
        output = catAppFileOnEmulator("android", "TNSApp", "app/test.css")
        assert ("color: #284848;" in output)
        output = catAppFileOnEmulator("android", "TNSApp", "app/test/main-view-model.js")
        assert ("HelloWorldModel.prototype.tapAction" in output)

    @unittest.skip("TODO: Fix this test.")
    def test_202_LiveSync_Android_Watch(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")

#         print "tns livesync android --watch --path TNS_App"
#         pr = subprocess.Popen("tns livesync android --watch --path TNS_App", shell=True)
#         pr_pid = pr.pid
#  
#         time.sleep(60)
#         print "assert"
#         output = catAppFile("android", "TNSApp", "app/main-page.xml")
#         assert ("<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output)
#  
#         time.sleep(5)
#         replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")
#  
#         time.sleep(15)
#         print "assert"
#         output = catAppFile("android", "TNSApp", "app/main-page.xml")
#         assert ("<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output)
#  
#         time.sleep(5)
#         replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")
#  
#         time.sleep(15)
#         print "assert"
#         output = catAppFile("android", "TNSApp", "app/main-page.xml")
#         assert ("<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output)
#  
#         print "killing child ..."
#         pr.terminate()
#  
#         time.sleep(5)
#         if psutil.pid_exists(pr_pid):
#             print "force killing child ..."
#             pr.kill()

    def test_301_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", device="emulator-5554", path="TNS_App")

        time.sleep(3)
        output = catAppFileOnEmulator("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

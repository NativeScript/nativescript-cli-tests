import unittest
import os, psutil, shutil, subprocess, time

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRealDeviceRunning, StopEmulators, \
    StopSimulators

class LiveSync_Android(unittest.TestCase):

    # LiveSync Tests on Android Device

    @classmethod
    def setUpClass(cls):
        StopEmulators()
        StopSimulators()

        CleanupFolder('./TNS_App')
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        GivenRealDeviceRunning(platform="android")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_001_LiveSync_Android_XmlJsCss_Files(self):

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

    # This test executes the Run -> LiveSync -> Run workflow on an android device with API level 21. 
    def test_002_LiveSync_Android_Device_XmlFile_Run(self):

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", device="030b206908e6c3c5", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

        replace("TNS_App/app/main-page.xml", "TEST", "RUN")
        Run(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"RUN\" tap=\"{{ tapAction }}\" />" in output)

    @unittest.skip("TODO: Fix this test.")
    def test_004_LiveSync_Android_Watch(self):

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
        
        # TODO: Add test for synch css and platform specific files (.android and .ios)
        time.sleep(5)
        if psutil.pid_exists(pr_pid):
            print "force killing child ..."
            pr.kill()

    def test_011_LiveSync_Android_TnsModules_Files(self):

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace("TNS_App/node_modules/tns-core-modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")
        LiveSync(platform="android", path="TNS_App")
        time.sleep(5)
        
        output = catAppFile("android", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)

        output = catAppFile("android", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    def test_021_LiveSync_Android_AddNewFiles(self):

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")
        LiveSync(platform="android", path="TNS_App")
        time.sleep(5)
                
        output = catAppFile("android", "TNSApp", "app/test.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
        output = catAppFile("android", "TNSApp", "app/test.js")
        assert ("page.bindingContext = vmModule.mainViewModel;" in output)
        output = catAppFile("android", "TNSApp", "app/test.css")
        assert ("color: #284848;" in output)

    @unittest.skip("Not implemented.")
    def test_031_LiveSync_Android_DeleteFiles(self):

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

    def test_302_LiveSync(self):

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        output = LiveSync(path="TNS_App", assertSuccess=False)

        assert ("Multiple device platforms detected (iOS and Android). Specify platform or device on command line." in output)

#     # TODO: Implement it.
#     @unittest.skip("Fix LiveSync for Android device.")
#     def test_101_LiveSync_Android_MultipleDevice(self):
#         CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
#         Run(platform="android", path="TNS_App")
#  
#         replace("TNS_App/app/main-view-model.js", "taps", "clicks")
#         LiveSync(platform="android", path="TNS_App")
# 
#         # TODO: Assert both emulator and device
#         output = catAppFile("android", "TNSApp", "app/main-view-model.js")
#         assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
# 
#     # TODO:
#     # - test to detect a deleted file
#     # - test to check change in a file that is not being used will not affect the app
#     # - test to check JavaScript, XML and CSS do not crash the app

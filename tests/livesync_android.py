import unittest
import os, psutil, shutil, subprocess, time

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRealDeviceRunning

class LiveSync_Android(unittest.TestCase):

    # LiveSync Tests on Android Device

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

    def test_001_LiveSync_Android_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_002_LiveSync_Android_Device_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", device="030b206908e6c3c5", path="TNS_App")

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

    def test_011_LiveSync_Android_JsFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)

    def test_012_LiveSync_Android_CssFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/app.css", "30", "20")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/app.css")
        assert ("font-size: 20;" in output)

    def test_013_LiveSync_Android_TnsModules_File(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/tns_modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    def test_014_LiveSync_Android_TnsModules_LICENSE(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/tns_modules/LICENSE", "2015", "9999")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)

    def test_021_LiveSync_Android_AddNewFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")
        LiveSync(platform="android", path="TNS_App")

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

    def test_302_LiveSync_XmlFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_303_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        LiveSync(path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)

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

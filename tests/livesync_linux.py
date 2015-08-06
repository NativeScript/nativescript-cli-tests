import unittest
import psutil, subprocess, time

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRunningEmulator

class LiveSync_Linux(unittest.TestCase):

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
        LiveSync(platform="android", device="emulator-5554", path="TNS_App")
 
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    @unittest.skip("TODO: Fix.")
    def test_003_LiveSync_Android_Watch(self):
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

    def test_005_LiveSync_Android_JsFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
 
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="android", path="TNS_App")
 
        output = catAppFile("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)

    def test_006_LiveSync_Android_CssFile(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
 
        replace("TNS_App/app/app.css", "30", "50")
        LiveSync(platform="android", path="TNS_App")
 
        output = catAppFile("android", "TNSApp", "app/app.css")
        assert ("font-size: 50;" in output)

    def test_007_LiveSync_Android_TnsModule_File(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/tns_modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/tns_modules/application/application-common.js")
        assert ("require(\"globals\"); // test" in output)

    def test_008_LiveSync_Android_TnsModule_LICENSE(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/tns_modules/LICENSE", "2015", "9999")
        LiveSync(platform="android", path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/tns_modules/LICENSE")
        assert ("Copyright (c) 9999 Telerik AD" in output)

    def test_301_LiveSync(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(path="TNS_App")
  
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_302_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        LiveSync(path="TNS_App")

        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)

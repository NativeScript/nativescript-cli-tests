import unittest
import psutil, subprocess, time

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, iosRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRealDeviceRunning

class LiveSync_OSX(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App');
        GivenRealDeviceRunning(platform="ios")
        GivenRealDeviceRunning(platform="android")

    def tearDown(self):
        pass

    def test_001_LiveSync_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="ios", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_002_LiveSync_iOS_Device(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")

        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="ios", device="a0036be7bace11a09a86fd5a31fca9c8c105011f", path="TNS_App")

        output = catAppFile("ios", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)

    @unittest.skip("TODO: Fix.")
    def test_003_LiveSync_iOS_Watch(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        Run(platform="ios", path="TNS_App")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")

        pr = subprocess.Popen("tns livesync ios --watch --path TNS_App", shell=True)
        pr_pid = pr.pid

        time.sleep(60)
        print "assert"
        output = catAppFile("ios", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output)

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")

        time.sleep(15)
        print "assert"
        output = catAppFile("ios", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output)

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")

        time.sleep(15)
        print "assert"
        output = catAppFile("ios", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output)

        print "killing child ..."
        pr.terminate()

        time.sleep(5)
        if psutil.pid_exists(pr_pid):
            print "force killing child ..."
            pr.kill()

    @unittest.skip("Fix LiveSync for Android device.")  
    def test_101_LiveSync_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
 
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", path="TNS_App")
 
        output = catAppFile("android", "TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    @unittest.skip("Fix LiveSync for Android device.")
    def test_102_LiveSync_Android_Device(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
   
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="android", device="030b206908e6c3c5", path="TNS_App")
   
        output = catAppFile("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)

    @unittest.skip("Fix LiveSync for Android device.")
    def test_103_LiveSync_Android_Watch(self):
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

    def test_301_LiveSync_MultiplePlatforms(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        output = LiveSync(path="TNS_App", assertSuccess=False)
        assert ("Multiple device platforms detected (iOS and Android). Specify platform or device on command line." in output)

import unittest
import logging, time, threading

from helpers._os_lib import CleanupFolder, runAUT, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, tnsPath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRunningEmulator, GivenRealDeviceRunning

class LiveSync_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')
        # linux
        GivenRunningEmulator()
        # osx
        # GivenRealDeviceRunning(platform="android")

    logging.basicConfig(level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',)

    def tearDown(self):
        pass

    def test_001_LiveSync_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
 
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform="android", path="TNS_App")
 
        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
 
    def test_002_LiveSync_Android_Device(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
 
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="android", device="emulator-5554", path="TNS_App")
 
        output = catAppFile("TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)

    def test_003_LiveSync_Android_Watch(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android")#, frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        def watch():
            time.sleep(38)
            logging.debug("assert")
#             output = catAppFile("TNSApp", "app/main-page.xml")
#             output = runAUT("adb shell run-as org.nativescript.TNSApp cat files/app/main-page.xml", getOutput=False)
#             assert ("<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output)

            time.sleep(1)
            logging.debug("replace")
            replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")

            time.sleep(10)
            logging.debug("assert")
#             output = catAppFile("TNSApp", "app/main-page.xml")
#             output = runAUT("adb shell run-as org.nativescript.TNSApp cat files/app/main-page.xml", getOutput=False)
#             assert ("<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output)

            time.sleep(1)
            logging.debug("replace")
            replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")

            time.sleep(10)
            logging.debug("assert")
#             output = catAppFile("TNSApp", "app/main-page.xml")
#             output = runAUT("adb shell run-as org.nativescript.TNSApp cat files/app/main-page.xml", getOutput=False)
#             assert ("<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output)

        thread =  threading.Thread(target=watch)
        thread.daemon = True
        thread.start()

        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")
        LiveSync(watch=True, path="TNS_App")

        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output)

    def test_301_LiveSync(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(path="TNS_App")
  
        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_302_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        output = runAUT(tnsPath + " livesync --path TNS_App")

        assert ("Project successfully prepared" in output)
        assert ("Project successfully built" in output)
        assert ("Successfully deployed on device with identifier" in output)

        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)

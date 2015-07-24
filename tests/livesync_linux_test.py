import unittest
import logging, time, threading

from helpers._os_lib import CleanupFolder, runAUT, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
    CreateProjectAndAddPlatform, LiveSync, Run
from helpers.device import GivenRunningEmulator#, GivenRealDeviceRunning

class LiveSync_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')
        GivenRunningEmulator()
        #GivenRealDeviceRunning(platform="android")

    def tearDown(self):
        pass

    logging.basicConfig(level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',)

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
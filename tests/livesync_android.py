import unittest
import logging

from helpers._os_lib import CleanupFolder, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, \
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
        GivenRunningEmulator()
        GivenRealDeviceRunning(platform="android")

    logging.basicConfig(level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',)

    def tearDown(self):
        pass

    # TODO: Implement it.
    @unittest.skip("Fix LiveSync for Android device.")
    def test_101_LiveSync_Android_MultipleDevice(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        Run(platform="android", path="TNS_App")
 
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform="android", path="TNS_App")

        # TODO: Assert both emulator and device
        output = catAppFile("android", "TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)

    # TODO:
    # - test to detect a new/deleted file
    # - test to check change in a file that is not being used will not affect the app
    # - test to check JavaScript, XML and CSS do not crash the app

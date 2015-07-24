import unittest

from helpers._os_lib import CleanupFolder, runAUT, replace, catAppFile
from helpers._tns_lib import androidRuntimePath, tnsPath, \
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

    def test_001_LiveSync_Android(self):
        CreateProjectAndAddPlatform(projName = "TNS_App", platform = "android")#, frameworkPath = androidRuntimePath)
        Run(platform = "android", path = "TNS_App")
 
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(platform = "android", path = "TNS_App")
 
        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)
 
    def test_002_LiveSync_Android_Device(self):
        CreateProjectAndAddPlatform(projName = "TNS_App", platform = "android")#, frameworkPath = androidRuntimePath)
        Run(platform = "android", path = "TNS_App")
 
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        LiveSync(platform = "android", device = "emulator-5554", path = "TNS_App")
 
        output = catAppFile("TNSApp", "app/main-view-model.js")
        assert ("this.set(\"message\", this.counter + \" clicks left\");" in output)
 
    def test_003_LiveSync_Android_Watch(self):
        pass
 
    def test_301_LiveSync(self):
        CreateProjectAndAddPlatform(projName = "TNS_App", platform = "android")#, frameworkPath = androidRuntimePath)
        Run(platform = "android", path = "TNS_App")
  
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        LiveSync(path = "TNS_App")
  
        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output)

    def test_302_LiveSync_BeforeRun(self):
        CreateProjectAndAddPlatform(projName = "TNS_App", platform = "android")#, frameworkPath = androidRuntimePath)
        output = runAUT(tnsPath + " livesync --path TNS_App")

        assert ("Project successfully prepared" in output)
        assert ("Project successfully built" in output)
        assert ("Successfully deployed on device with identifier" in output)

        output = catAppFile("TNSApp", "app/main-page.xml")
        assert ("<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output)
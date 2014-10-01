import os
import unittest

from helpers._os_lib import runAUT, CleanupFolder
from helpers._tns_lib import CreateProject
from helpers.emulator import StopEmulators


class TNSTests_Android(unittest.TestCase):

    tnsPath = os.path.join('node_modules', '.bin', 'tns');
    nativescriptPath = os.path.join('node_modules', '.bin', 'nativescript');

    def setUp(self):
        print "#####"
        print "Cleanup test folders started..."
        CleanupFolder('./folder');
        CleanupFolder('./TNS_Javascript');
        print "Cleanup test folders completed!"
        print "#####"
        
        print self.id()

    def tearDown(self):
        StopEmulators()
                      
    def test_030_PlatformList(self):        
                
        CreateProject("TNS_Javascript")
        
        command = self.tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Available platforms for this OS:  android" in output)      
        assert ("No installed platforms found. Use $ tns platform add" in output)    
        assert not ("Error" in output)  
        
    #===========================================================================
    # Currently we execute this test list on all platforms and we can not run this test on Windows
    # TODO: Separate iOS test in another test suite.
    # def test_052_PlatformRemoveIOS(self):
    #     command = self.tnsPath + " platform remove ios"
    #     output = runAUT(command)     
    #     assert not ("Error" in output)           
    #===========================================================================

    #===========================================================================
    # Currently we execute this test list on all platforms and we can not run this test on Windows
    # TODO: Separate iOS test in another test suite.
    # def test_062_PreparePlatformIOS(self):
    #     command = self.tnsPath + " prepare ios"
    #     output = runAUT(command)     
    #     assert not ("Error" in output)  
    #===========================================================================

    #===========================================================================
    # Currently we execute this test list on all platforms and we can not run this test on Windows
    # TODO: Separate iOS test in another test suite.
    # def test_072_BuildPlatformIOS(self):
    #     command = self.tnsPath + " build ios"
    #     output = runAUT(command)     
    #     assert not ("Error" in output)  
    #===========================================================================

    #===============================================================================
    # Currently we have no emulators on some of the test agents. 
    # TODO: Install emulators on all test agents.
    #     def test_081_EmulatePlatformAndroid(self):
    # 
    #         self.test_061_PreparePlatformAndroid()
    #                 
    #         command = self.tnsPath + " emulate android --path TNS_Javascript"
    #         output = runAUT(command)     
    #         assert ("BUILD SUCCESSFUL" in output) 
    #         assert not ("Error" in output) 
    #         
    #         time.sleep(5)
    #         
    #     if "win" in platform.uname():
    #         runAUT("taskkill /IM emulator-x86.exe")
    #     else:
    #         runAUT("adb -s emulator-5554 emu kill")                
    #===============================================================================
 
    #===========================================================================
    # Currently we execute this test list on all platforms and we can not run this test on Windows
    # TODO: Separate iOS test in another test suite.
    # def test_082_EmulatePlatformIOS(self):
    #     command = self.tnsPath + " emulate ios"
    #     output = runAUT(command)     
    #     assert not ("Error" in output)  
    #===========================================================================

    #===========================================================================
    # Currently we have no emulators on some of the test agents. 
    # TODO: Install emulators on all test agents.
    # def test_091_DeployPlatformAndroid(self):
    #     command = self.tnsPath + " deploy android"
    #     output = runAUT(command)     
    #     assert not ("Error" in output)                    
    #===========================================================================
 
    #===========================================================================
    # Currently we execute this test list on all platforms and we can not run this test on Windows
    # TODO: Separate iOS test in another test suite.
    # def test_092_DeployPlatformIOS(self):
    #     command = self.tnsPath + " deploy ios"
    #     output = runAUT(command)     
    #     assert not ("Error" in output) 
    #===========================================================================
  
    #===========================================================================
    # Currently we have no emulators on some of the test agents. 
    # TODO: Install emulators on all test agents.
    # def test_100_RunPlatform(self):
    #     command = self.tnsPath + " run"
    #     output = runAUT(command)     
    #     assert not ("Error" in output) 
    #===========================================================================
         
    #===========================================================================
    # Currently we have no emulators on some of the test agents. 
    # TODO: Install emulators on all test agents.
    # def test_101_RunPlatformAndroid(self):
    #     command = self.tnsPath + " run android"
    #     output = runAUT(command)     
    #     assert not ("Error" in output)                    
    #===========================================================================
 
    #===========================================================================
    # Currently we execute this test list on all platforms and we can not run this test on Windows
    # TODO: Separate iOS test in another test suite.
    # def test_102_RunPlatformIOS(self):
    #     command = self.tnsPath + " run ios"
    #     output = runAUT(command)     
    #     assert not ("Error" in output) 
    #===========================================================================

import unittest

from helpers._os_lib import runAUT, CleanupFolder, KillProcess, WaitForProcess
from helpers._tns_lib import CreateProject, tnsPath
from helpers.emulator import StopEmulators


class TNSTests_OSX(unittest.TestCase):

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
        
        command = tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Available platforms for this OS:  ios and android" in output)      
        assert ("No installed platforms found. Use $ tns platform add" in output)    
        assert not ("Error" in output)  
 
    def test_042_PlatformAddIOS(self):        
                
        CreateProject("TNS_Javascript")
        
        command = tnsPath + " platform add ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Copying template files..." in output)
        assert ("Project successfully created." in output)
        assert not ("Error" in output)  
        
    def test_052_PlatformRemoveIOS(self):        
                
        CreateProject("TNS_Javascript")
        
        command = tnsPath + " platform remove ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("The platform ios is not added to this project. Please use 'tns platform add <platform>'" in output)

        command = tnsPath + " platform add ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully created." in output)     
        
        command = tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Installed platforms:  ios" in output)    
        
        command = tnsPath + " platform remove ios --path TNS_Javascript"
        output = runAUT(command)     
        assert not ("Error" in output)    
        
        command = tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command)     
        assert ("No installed platforms found. Use $ tns platform add" in output)  

    def test_062_PreparePlatformIOS(self):        
                
        self.test_042_PlatformAddIOS();
        
        command = tnsPath + " prepare ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully prepared" in output)

    def test_072_BuildPlatformIOS(self):        
                
        self.test_062_PreparePlatformIOS();
        
        command = tnsPath + " build ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully built" in output)

    def test_082_EmulatePlatformIOS(self):        
                
        KillProcess("iOS Simulator")        
        self.test_062_PreparePlatformIOS();
        
        command = tnsPath + " emulate ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully built" in output)
        assert ("Starting iOS Simulator" in output)
        
        assert (WaitForProcess("iOS Simulator"))
        KillProcess("iOS Simulator")

#===============================================================================
#     def test_092_DeployPlatformIOS(self):        
#                 
#         KillProcess("iOS Simulator")
#         
#         self.test_062_PreparePlatformIOS();
#         
#         command = tnsPath + " deploy ios --path TNS_Javascript"
#         output = runAUT(command)     
#         
#         assert (IsRunningProcess("iOS Simulator"))
# 
#     def test_102_RunPlatformIOS(self):        
#                 
#         KillProcess("iOS Simulator")
#         
#         self.test_062_PreparePlatformIOS();
#         
#         command = tnsPath + " run ios --path TNS_Javascript"
#         output = runAUT(command)     
#         
#         assert (IsRunningProcess("iOS Simulator"))
#===============================================================================
                                                 
    def test_112_ListDevicesiOS(self):
                
        command = tnsPath + " list-devices ios"
        output = runAUT(command)     
        
        assert not ("Error" in output)  
        assert not ("Android" in output)
import unittest

from helpers._os_lib import runAUT, CleanupFolder, KillProcess
from helpers._tns_lib import CreateProject, tnsPath, AddPlatform, GetIOSFrameworkPath
from helpers.emulator import StopEmulators

# This class runs only on OSX test nodes
class TNSTests_OSX(unittest.TestCase):

    def setUp(self):
        print "#####"
        print "Cleanup test folders started..."
        CleanupFolder('./folder');
        CleanupFolder('./TNS_Javascript');
        runAUT("sudo find /var/folders/ -name '*TNS_Javascript-*' -exec rm -rf {} \;") # Delete precompiled headers
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
        output = AddPlatform("ios", GetIOSFrameworkPath(), "TNS_Javascript");    
        assert ("Copying template files..." in output)
        assert ("Project successfully created." in output)
        assert not ("Error" in output)  
        
    def test_052_PlatformRemoveIOS(self):        
                
        CreateProject("TNS_Javascript")
        
        command = tnsPath + " platform remove ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("The platform ios is not added to this project. Please use 'tns platform add <platform>'" in output)

        output = AddPlatform("ios", GetIOSFrameworkPath(), "TNS_Javascript"); 
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
        
        command = tnsPath + " emulate ios --emulator --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully built" in output)
        assert ("Starting iOS Simulator" in output)
        
        KillProcess("iOS Simulator")

    def test_092_DeployPlatformIOS(self):        
                 
        KillProcess("iOS Simulator")
         
        self.test_062_PreparePlatformIOS();
        
        command = "security unlock-keychain -p '' $KEYCHAIN"
        runAUT(command)  
        
        command = tnsPath + " deploy ios --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully built" in output)
        assert ("Successfully deployed" in output)
                
        KillProcess("iOS Simulator")
 
    def test_102_RunPlatformIOS(self):        
                 
        KillProcess("iOS Simulator")
         
        self.test_062_PreparePlatformIOS();
         
        command = tnsPath + " run ios --emulator --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Project successfully built" in output)
        assert ("Starting iOS Simulator" in output)
         
        KillProcess("iOS Simulator")
                                                 
    def test_112_ListDevicesiOS(self):
                
        command = tnsPath + " device ios"
        output = runAUT(command)     
        
        assert ("iOS" in output)
        assert not ("Error" in output)
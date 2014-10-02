import unittest

from helpers._os_lib import runAUT, CleanupFolder
from helpers._tns_lib import CreateProject, tnsPath
from helpers.emulator import StopEmulators


class TNSTests_Android(unittest.TestCase):

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
        assert ("Available platforms for this OS:  android" in output)      
        assert ("No installed platforms found. Use $ tns platform add" in output)    
        assert not ("Error" in output)  

    def test_111_ListDevicesAndroid(self):
                
        command = tnsPath + " list-devices android"
        output = runAUT(command)     
        
        assert ("Cannot find connected devices." in output) 
        assert ("Reconnect any connected devices, verify that your system recognizes them, and run this command again" in output)     
        assert not ("Error" in output)
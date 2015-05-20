import unittest

from helpers._os_lib import runAUT
from helpers._tns_lib import tnsPath

class Autocomplete(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):        
        pass

    def test_001_Autocomplete_Enable(self):
        output = runAUT(tnsPath + " autocomplete status")
        
        if ("Autocompletion is disabled." in output):
            output = runAUT(tnsPath + " autocomplete enable --log trace")
            assert ("Restart your shell to enable command auto-completion." in output)

        #if ("Autocompletion is enabled." in output):
        else:
            output = runAUT(tnsPath + " autocomplete enable --log trace")
            assert ("Autocompletion is already enabled." in output)
        
        output = runAUT(tnsPath + " autocomplete status")
        assert ("Autocompletion is enabled." in output)    
 
    def test_002_Autocomplete_Disable(self):
        output = runAUT(tnsPath + " autocomplete status")
        
        if ("Autocompletion is enabled." in output):
            output = runAUT(tnsPath + " autocomplete disable")   
            assert ("Restart your shell to disable command auto-completion." in output)    
        
        #if ("Autocompletion is disabled." in output):
        else:
            output = runAUT(tnsPath + " autocomplete disable")
            assert ("Autocompletion is already disabled." in output)
        
        output = runAUT(tnsPath + " autocomplete status")   
        assert ("Autocompletion is disabled." in output)    
                
    def test_400_Autocomplete_WithInvalidParameter(self):
        command = tnsPath + " autocomplete invalidParam"
        output = runAUT(command)   
        assert ("The input is not valid sub-command for 'autocomplete' command" in output)
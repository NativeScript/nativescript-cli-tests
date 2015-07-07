import unittest

from helpers._os_lib import runAUT
from helpers._tns_lib import tnsPath


class UsageAndErrorTracking(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):        
        pass

    def test_001_FeatureUsageTracking(self):
        output = runAUT(tnsPath + " usage-reporting")   
        assert ("Usage reporting is" in output)    
        
    def test_002_FeatureUsageTracking_Enable(self):
        output = runAUT(tnsPath + " usage-reporting enable")   
        assert ("Usage reporting is now enabled." in output)    
        
        output = runAUT(tnsPath + " usage-reporting status")   
        assert ("Usage reporting is enabled." in output)    
 
    def test_003_FeatureUsageTracking_Disable(self):
        output = runAUT(tnsPath + " usage-reporting disable")   
        assert ("Usage reporting is now disabled." in output)    
        
        output = runAUT(tnsPath + " usage-reporting status")   
        assert ("Usage reporting is disabled." in output)    

    def test_100_ErrorReporting(self):
        output = runAUT(tnsPath + " error-reporting")   
        assert ("Error reporting is" in output)    
        
    def test_101_ErrorReporting_Enable(self):
        output = runAUT(tnsPath + " error-reporting enable")   
        assert ("Error reporting is now enabled." in output)    
        
        output = runAUT(tnsPath + " error-reporting status")   
        assert ("Error reporting is enabled." in output)    
 
    def test_102_ErrorReporting_Disable(self):
        output = runAUT(tnsPath + " error-reporting disable")   
        assert ("Error reporting is now disabled." in output)    
        
        output = runAUT(tnsPath + " error-reporting status")   
        assert ("Error reporting is disabled." in output)    
                        
    def test_400_FeatureUsageTracking_WithInvalidParameter(self):
        command = tnsPath + " usage-reporting invalidParam"
        output = runAUT(command)   
        assert ("The value 'invalidParam' is not valid. Valid values are 'enable', 'disable' and 'status'" in output)
        
    def test_401_ErrorReporting_WithInvalidParameter(self):
        command = tnsPath + " error-reporting invalidParam"
        output = runAUT(command)   
        assert ("The value 'invalidParam' is not valid. Valid values are 'enable', 'disable' and 'status'" in output)        
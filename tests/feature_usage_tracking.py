import unittest

from helpers._os_lib import runAUT, CheckOutput
from helpers._tns_lib import tnsPath


class FeatureUsageTracking(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):        
        pass

    def test_010_FeatureUsageTracking(self):
        output = runAUT(tnsPath + " feature-usage-tracking")   
        assert ("Feature usage tracking is" in output)    
        
    def test_011_FeatureUsageTracking_Enable(self):
        output = runAUT(tnsPath + " feature-usage-tracking enable")   
        assert ("Feature usage tracking is now enabled." in output)    
        
        output = runAUT(tnsPath + " feature-usage-tracking status")   
        assert ("Feature usage tracking is enabled." in output)    
 
    def test_012_FeatureUsageTracking_Disable(self):
        output = runAUT(tnsPath + " feature-usage-tracking disable")   
        assert ("Feature usage tracking is now disabled." in output)    
        
        output = runAUT(tnsPath + " feature-usage-tracking status")   
        assert ("Feature usage tracking is disabled." in output)    
                
    def test_400_FeatureUsageTracking_WithInvalidParameter(self):
        command = tnsPath + " feature-usage-tracking invalidParam"
        output = runAUT(command)   
        assert ("The value 'invalidParam' is not valid. Valid values are 'enable', 'disable' and 'status'" in output)  
        assert CheckOutput(output, 'feature_help_output.txt')
import unittest

from helpers._os_lib import CleanupFolder


class Debug_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    #TODO: Implement this test 
    @unittest.skip("Not implemented.")  
    def test_001_Debug_iOS(self):
        pass

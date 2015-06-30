import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimePath, \
    tnsPath, CreateProject, androidRuntimePath, PlatformAdd


class Init_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_001_Init_Defaults(self):
        pass

    def test_002_Init_PackageJSON(self):
        pass
                
    def test_003_Init_Path(self):
        pass
    
    def test_004_Init_CopyFrom(self):
        pass
        
    def test_400_Init_MissingPackgeJSON(self):
        pass

    def test_401_Init_InvalidPackageJSON(self):
        pass       
        
    def test_403_Init_InvalidPath(self):
        pass
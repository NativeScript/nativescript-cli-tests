import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimePath, \
    tnsPath, CreateProject, androidRuntimePath, PlatformAdd


class Install_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_001_Install_Defaults(self):
        pass

    def test_002_Install_PackageJSON(self):
        pass
                
    def test_003_Install_Path(self):
        pass
    
    def test_004_Install_CopyFrom(self):
        pass
        
    def test_400_Install_MissingPackgeJSON(self):
        pass

    def test_401_Install_InvalidPackageJSON(self):
        pass       
        
    def test_403_Install_InvalidPath(self):
        pass
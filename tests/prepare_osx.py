import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimeSymlinkPath, \
    tnsPath


class Prepare_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_010_Prepare_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert("Project successfully prepared" in output)

        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/ios/TNS_App/app/bootstrap.js')
        assert FileExists('TNS_App/platforms/ios/TNS_App/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNS_App/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNS_App/tns_modules/application/application.ios.js')
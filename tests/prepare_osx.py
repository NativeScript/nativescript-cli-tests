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
        CleanupFolder('./TNS_App');

    def test_001_Prepare_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert("Project successfully prepared" in output)

        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

    def test_200_Prepare_Additional_AppResources_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        
        # Create new files in AppResources
        runAUT("cp TNS_App/app/App_Resources/iOS/Default.png TNS_App/app/App_Resources/iOS/newDefault.png")
        
        # Prepare project
        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert("Project successfully prepared" in output)

        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')
        
        # Verify XCode Project include files from App Resources folder
        runAUT("cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep newDefault.png")
        assert ("newDefault.png" in output)
               
    def test_300_Prepare_iOS_PreserveCase(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        runAUT("cp TNS_App/app/tns_modules/application/application-common.js TNS_App/app/tns_modules/application/New-application-common.js")
        runAUT("cp TNS_App/app/tns_modules/application/application.android.js TNS_App/app/tns_modules/application/New-application.android.js")
        runAUT("cp TNS_App/app/tns_modules/application/application.ios.js TNS_App/app/tns_modules/application/New-application.ios.js")
        
        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert("Project successfully prepared" in output)

        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')
        
        # Verify case is preserved
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application-common.js')
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.ios.js')
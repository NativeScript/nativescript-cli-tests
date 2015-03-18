import os
import unittest

from helpers._os_lib import runAUT, CleanupFolder, CheckFilesExists, \
    IsEmpty, FileExists
from helpers._tns_lib import tnsPath, CreateProject, PlatformAdd, \
    iosRuntimePath, iosRuntimeSymlinkPath, CreateProjectAndAddPlatform, Prepare, \
    androidRuntimePath


class Platform_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_001_Platform_List_IOS_Project(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        output = runAUT(tnsPath + " platform list --path TNS_App")   
        assert ("The project is not prepared for any platform" in output)
        assert ("Installed platforms:  ios" in output)
           
        Prepare(path="TNS_App", platform="ios") 
        output = runAUT(tnsPath + " platform list --path TNS_App")   
        assert ("The project is prepared for:  ios" in output)
        assert ("Installed platforms:  ios" in output)
        
        PlatformAdd(platform="android", frameworkPath=androidRuntimePath, path="TNS_App", symlink=True)
        output = runAUT(tnsPath + " platform list --path TNS_App")   
        assert ("The project is prepared for:  ios" in output)
        assert ("Installed platforms:  android and ios" in output)

        Prepare(path="TNS_App", platform="android")
        output = runAUT(tnsPath + " platform list --path TNS_App")   
        assert ("The project is prepared for:  ios and android" in output)
        assert ("Installed platforms:  android and ios" in output)
                        
    def test_002_Platform_Add_iOS(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_live.txt')
        
    def test_003_Platform_Add_iOS_Symlink(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", path="TNS_App", symlink=True)
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_symlink.txt')
        
        # Verify Runtime is symlink
        output = runAUT("ls -la TNS_App/platforms/ios/")
        assert ("Metadata ->" in output)
        assert ("package/framework/Metadata" in output)

    def test_004_Platform_Add_iOS_Symlink_And_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", path="TNS_App", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_symlink.txt')
        
        # Verify Runtime is symlink
        output = runAUT("ls -la TNS_App/platforms/ios/")
        assert ("Metadata ->" in output)
        assert ("package/framework/Metadata" in output)
       
    def test_200_Platform_Add_iOS_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", frameworkPath=iosRuntimePath, path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_current.txt')
        
        # If project.xcworkspace is there Xcode project name is wrong
        assert not FileExists("TNS_App/platforms/ios/TNS_App.xcodeproj/project.xcworkspace")
        
    def test_201_Platform_Remove_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimePath)
        output = runAUT(tnsPath + " platform remove ios --path TNS_App")        
        assert not ("error" in output)
        assert IsEmpty('TNS_App/platforms')
        # TODO: Add more verifications after https://github.com/NativeScript/nativescript-cli/issues/281 is fixed

    def test_202_Platform_Remove_iOS_Symlink(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        output = runAUT(tnsPath + " platform remove ios --path TNS_App")        
        assert not ("error" in output)
        assert IsEmpty('TNS_App/platforms')
        # TODO: Add more verifications after https://github.com/NativeScript/nativescript-cli/issues/281 is fixed

    #TODO: Implement this test 
    @unittest.skip("Not implemented.")      
    def test_203_Platform_Update_iOS(self):
        pass
        
    def test_400_Platform_Add_AlreadyExistingPlatform(self):
        self.test_020_Platform_Add_iOS()     
        
        output = runAUT(tnsPath + " platform add ios --path TNS_App")
        assert("Platform ios already added" in output)
        assert("Usage" in output)
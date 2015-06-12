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
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_1.1.0.txt')
        
    def test_003_Platform_Add_iOS_Symlink(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", path="TNS_App", symlink=True)
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_symlink.txt')
        
        # Verify Runtime is symlink
        output = runAUT("ls -la TNS_App/platforms/ios/")
        assert ("NativeScript.framework ->" in output)
        assert ("package/framework/NativeScript.framework" in output)

    def test_004_Platform_Add_iOS_Symlink_And_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", path="TNS_App", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_symlink.txt')
        
        # Verify Runtime is symlink
        output = runAUT("ls -la TNS_App/platforms/ios/")
        assert ("NativeScript ->" in output)
        assert ("package/framework/NativeScript" in output)
       
    def test_200_Platform_Add_iOS_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios", frameworkPath=iosRuntimePath, path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_current.txt')
       
        # If project.xcworkspace is there Xcode project name is wrong
        assert not FileExists("TNS_App/platforms/ios/TNSApp.xcodeproj/project.xcworkspace")
 
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

    def test_203_Platform_Update_iOS(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios@1.0.0", path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.0.0\"" in output)

        output = runAUT(tnsPath + " platform update ios@1.0.1 --path TNS_App")  
        assert ("We need to override xcodeproj file. The old one will be saved at" in output)
        
        output = runAUT("echo '' | " + tnsPath + " platform update ios@1.0.1 --path TNS_App")  
        assert ("Successfully updated to version  1.0.1" in output)

        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.0.1\"" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_1.0.1.txt')
                    
    def test_204_Platform_Add_iOS_CustomVersion(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios@1.0.0", path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.0.0\"" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):
            assert CheckFilesExists('TNS_App/platforms/ios', 'platform_ios_1.0.0.txt')
 
    def test_205_Platform_Add_iOS_CustomExperimentalVersion(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="ios@0.9.2-exp-ios-8.2", path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"0.9.2-exp-ios-8.2\"" in output)

    def test_206_Platform_Add_iOS_CustomBundleId(self):
        # Create project with different appId
        CreateProject(projName = "TNS_App", appId="org.nativescript.MyApp")
        output = runAUT("cat TNS_App/package.json")
        assert ("\"id\": \"org.nativescript.MyApp\"" in output)

        # Add iOS platform
        output = PlatformAdd(platform="ios", path="TNS_App", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        assert("Project successfully created" in output)
  
        # Verify plist file 
        output = runAUT("cat TNS_App/platforms/ios/TNSApp/TNSApp-Info.plist")
        assert ("org.nativescript.MyApp" in output)
                                       
    def test_400_Platform_Add_AlreadyExistingPlatform(self):
        self.test_004_Platform_Add_iOS_Symlink_And_FrameworkPath()     
        
        output = runAUT(tnsPath + " platform add ios --path TNS_App")
        assert("Platform ios already added" in output)
        assert("Usage" in output)
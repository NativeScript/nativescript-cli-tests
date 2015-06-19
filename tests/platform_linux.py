import os
import platform
import unittest

from helpers._os_lib import runAUT, CleanupFolder, IsEmpty, \
    CheckFilesExists
from helpers._tns_lib import tnsPath, CreateProject, PlatformAdd, \
    androidRuntimePath, CreateProjectAndAddPlatform, androidRuntimeSymlinkPath


class Platform_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');
        
    def tearDown(self):        
        pass

    def test_001_Platform_List_EmptyProject(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " platform list --path TNS_App") 
               
        assert("No installed platforms found. Use $ tns platform add" in output)
        if 'Darwin' in platform.platform():
            assert("Available platforms for this OS:  ios and android" in output)
        else:
            assert("Available platforms for this OS:  android" in output)

    def test_002_Platform_Add_Android(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android", path="TNS_App")
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.1.0.txt')
        
    def test_003_Platform_Add_Android_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android", frameworkPath=androidRuntimePath, path="TNS_App")
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_current.txt')
    
    # Note: This test fails only on Windows.
    # TODO: Ignore tests at runtime (in tns_tests_runner.py). This will allow test to be ignored only on specific OS
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/282")    
    def test_004_Platform_Add_Android_Symlink(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android", path="TNS_App", symlink=True)
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created" in output)
        assert IsEmpty('TNS_App/platforms/android/assets')
        assert IsEmpty('TNS_App/platforms/android/libs')
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_symlink.txt')

    # Note: This test fails only on Windows.
    # TODO: Ignore tests at runtime (in tns_tests_runner.py). This will allow test to be ignored only on specific OS
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/282")       
    def test_005_Platform_Add_Android_Symlink_And_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android", path="TNS_App", frameworkPath=androidRuntimeSymlinkPath, symlink=True)
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created" in output)
        assert IsEmpty('TNS_App/platforms/android/assets')
        assert IsEmpty('TNS_App/platforms/android/libs')
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_symlink.txt')
       
    def test_200_Platform_List_InsideEmptyProject(self):
        CreateProject(projName="TNS_App")
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir,"TNS_App"))   
        output = runAUT(os.path.join("..", tnsPath) + " platform list")
        os.chdir(currentDir);
        
        assert("No installed platforms found. Use $ tns platform add" in output)
        if 'Darwin' in platform.platform():
            assert("Available platforms for this OS:  ios and android" in output)
        else:
            assert("Available platforms for this OS:  android" in output)  

    def test_201_Platform_Add_Android_InsideProject(self):
        CreateProject(projName="TNS_App")        
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir,"TNS_App"))        
        output = runAUT(os.path.join("..", tnsPath) + " platform add android")
        os.chdir(currentDir);
        
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.1.0.txt')

    def test_202_Platform_Remove_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        output = runAUT(tnsPath + " platform remove android --path TNS_App")        
        assert not ("error" in output)
        assert IsEmpty('TNS_App/platforms')
        # TODO: Add more verifications after https://github.com/NativeScript/nativescript-cli/issues/281 is fixed

    def test_203_Platform_Add_Android_CustomVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@0.9.0")               
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"0.9.0\"" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_0.9.0.txt')

    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/333") 
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/335")             
    def test_204_Platform_Update_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@0.4.2")               
        output = runAUT("cat TNS_App/.tnsproject")
        assert ("\"version\": \"0.4.2\"" in output)
        
        output = runAUT(tnsPath + " platform update android@1.0.0 --path TNS_App")        
        assert ("Successfully updated to version  1.0.0" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.0.0.txt')

    def test_205_Platform_Update_ToSameVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=None)
        output = runAUT(tnsPath + " platform update android --path TNS_App")        
        assert ("Current and new version are the same." in output)
        assert ("Usage" in output)
 
    def test_206_Platform_Update_ToOlderVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@0.9.0")               
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"0.9.0\"" in output)
        command = tnsPath + " platform update android@0.4.2 --path TNS_App"
        output = runAUT(command + "< enter_key.txt")
        assert ("You are going to downgrade to android runtime v.0.4.2. Are you sure?" in output)
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"0.9.0\"" in output)   
                                                  
    def test_207_SetSDK(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android --sdk 19", frameworkPath=androidRuntimePath, path="TNS_App")
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created" in output)
        output = runAUT("cat cat TNS_App/platforms/android/AndroidManifest.xml ")
        assert ("android:minSdkVersion=\"17\"" in output)      
        assert ("android:targetSdkVersion=\"19\"" in output)
               
    def test_400_Platform_List_WrongPath(self):
        output = runAUT(tnsPath + " platform list")
        assert("No project found at or above" in output)
        assert("and neither was a --path specified." in output)  
        
    def test_401_Platform_List_WrongPath(self):
        output = runAUT(tnsPath + " platform list --path invalidPath")
        assert("No project found at or above" in output)
        assert("and neither was a --path specified." in output)  
        
    def test_420_Platform_Add_AlreadyExistingPlatform(self):
        self.test_002_Platform_Add_Android()   
        
        output = runAUT(tnsPath + " platform add android --path TNS_App")
        assert("Platform android already added" in output)

    def test_421_Platform_Add_Android_WrongFrameworkPath(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform add android --frameworkPath invalidFile.tgz --path TNS_App")
        assert ("Error: ENOENT, stat '" in output)
        assert ("invalidFile.tgz" in output)
        assert ("Usage" in output)

    def test_423_Platform_Add_Android_WrongFrameworkPathOption(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform add android --frameworkpath tns-android.tgz --path TNS_App")
        assert ("The option 'frameworkpath' is not supported." in output)

    def test_424_Platform_Add_Android_WrongSymlinkOption(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform add android --frameworkPath tns-android.tgz --simlink --path TNS_App")
        assert ("The option 'simlink' is not supported." in output)

    def test_425_Platform_Add_EmptyPlatform(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform add --path TNS_App")
        assert ("No platform specified. Please specify a platform to add" in output)
        assert ("Usage" in output)
      
    def test_430_Platform_Remove_MissingPlatform(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform remove android --path TNS_App")
        assert ("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)
        assert ("Usage" in output)

    def test_431_Platform_Remove_InvalidPlatform(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform remove invalidPlatform --path TNS_App")
        assert ("Invalid platform invalidplatform. Valid platforms are ios or android." in output)
        assert ("Usage" in output)

    def test_432_Platform_Remove_EmptyPlatform(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform remove --path TNS_App")
        assert ("No platform specified. Please specify a platform to remove" in output)
        assert ("Usage" in output)
        
    def test_440_Platform_Update_MissingPlatform(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " platform update android --path TNS_App")
        assert ("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)
        assert ("Usage" in output)

    def test_441_Platform_Update_InvalidPlatform(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform update invalidPlatform --path TNS_App")
        assert ("Invalid platform invalidplatform. Valid platforms are ios or android." in output)
        assert ("Usage" in output)

    def test_442_Platform_Update_EmptyPlatform(self):
        CreateProject(projName="TNS_App")       
        output = runAUT(tnsPath + " platform update --path TNS_App")
        assert ("1mNo platform specified. Please specify platforms to update" in output)
        assert ("Usage" in output)
        
    def test_443_SetSDK_InvalidNewVersion(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android --sdk 29", frameworkPath=androidRuntimePath, path="TNS_App", assertSuccess=False)
        assert("You have selected to use android-29, but it is not currently installed." in output)
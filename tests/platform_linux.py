import os
import platform
import unittest

from helpers._os_lib import runAUT, CleanupFolder, IsEmpty, \
    CheckFilesExists
from helpers._tns_lib import androidRuntimePath, androidRuntimeSymlinkPath, Build, \
    tnsPath, CreateProject, CreateProjectAndAddPlatform, PlatformAdd
from time import sleep

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
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.3.0.txt')
        
    def test_003_Platform_Add_Android_FrameworkPath(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android", frameworkPath=androidRuntimePath, path="TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_current.txt')

    @unittest.skip("This test is not valid, adding symlink platform from npm cache cause issues")    
    def test_004_Platform_Add_Android_Symlink(self):
        if ('Windows' in platform.platform()):
            print "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282"
        else:
            CreateProject(projName="TNS_App")
            output = PlatformAdd(platform="android", path="TNS_App", symlink=True)
            assert("Copying template files..." in output)
            assert("Project successfully created" in output)
        
            if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
                assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_symlink.txt')

    def test_005_Platform_Add_Android_Symlink_And_FrameworkPath(self):
        if ('Windows' in platform.platform()):
            print "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282"
        else:
            CreateProject(projName="TNS_App")
            output = PlatformAdd(platform="android", path="TNS_App", frameworkPath=androidRuntimeSymlinkPath, symlink=True)
            assert("Copying template files..." in output)
            assert("Project successfully created" in output)
        
            if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
                assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_symlink.txt')
       
    def test_200_Platform_List_InsideEmptyProject(self):
        CreateProject(projName="TNS_App")
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
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
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " platform add android")
        os.chdir(currentDir);

        assert("Copying template files..." in output)
        assert("Project successfully created" in output)

        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.3.0.txt')

    def test_202_Platform_Remove_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)

        output = runAUT(tnsPath + " platform remove android --path TNS_App")
        assert ("Platform android successfully removed." in output)

        assert not ("error" in output)
        assert IsEmpty('TNS_App/platforms')

        output = runAUT("cat TNS_App/package.json")
        assert not ("tns-android" in output)

    def test_203_Platform_Add_Android_CustomVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@1.3.0")               
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.3.0\"" in output)
        
        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.3.0.txt')

    @unittest.skip("Ignonre because 1.3.0 do not support older versions, please enable after 1.3.1 is released")
    def test_204_Platform_Update_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@1.1.0")
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.1.0\"" in output)

        command = tnsPath + " platform update android@1.2.0 --path TNS_App"
        output = runAUT(command)
        assert ("Successfully updated to version  1.2.0" in output)

        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.2.0\"" in output)

        if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']) and ("2" in os.environ['ANDROID_HOME']):
            assert CheckFilesExists('TNS_App/platforms/android', 'platform_android_1.2.0.txt')
        Build(platform="android", path="TNS_App")

    def test_205_Platform_Update_Android_ToSameVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android")
        output = runAUT(tnsPath + " platform update android --path TNS_App")
        assert ("Current and new version are the same." in output)
        assert ("Usage" in output)
        Build(platform="android", path="TNS_App")

    @unittest.skip("Ignonre because 1.3.0 do not support older versions, please enable after 1.3.1 is released")
    def test_206_Platform_Downgrade_Android_ToOlderVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@1.2.0")
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.2.0\"" in output)

#         Comment these lines as they cause the test to fail
#         since commits in master on July 27, 2015
#         [31;1mCannot read property 'substring' of undefined[0m
#         TypeError: Cannot read property 'substring' of undefined

#         command = tnsPath + " platform update android@1.1.0 --path TNS_App"
#         output = runAUT(command + " < y_key.txt")
#         assert ("You are going to downgrade to android runtime v.1.1.0. Are you sure?" in output)
#         assert ("Successfully updated to version  1.1.0" in output)

        os.system(tnsPath + " platform update android@1.1.0 --path TNS_App < y_key.txt")
        sleep(10)
        
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.1.0\"" in output)
        Build(platform="android", path="TNS_App")

    @unittest.skip("Execute when platform update command starts respecting --frameworkPath.")
    def test_207_Platform_Update_Android_ToLatestVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android@1.0.0")
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.0.0\"" in output)

        command = tnsPath + " platform update android --frameworkPath {0} --path TNS_App".format(androidRuntimePath)
        output = runAUT(command)
        assert ("Successfully updated to version" in output)
        Build(platform="android", path="TNS_App")

    @unittest.skip("Skiped because of https://github.com/NativeScript/nativescript-cli/issues/784")
    def test_208_Platform_Downgrade_Android_FromLatestVersion(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)

        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1." in output)

#         Comment these lines as they cause the test to fail
#         since commits in master on July 27, 2015
#         [31;1mCannot read property 'substring' of undefined[0m
#         TypeError: Cannot read property 'substring' of undefined

#         command = tnsPath + " platform update android@1.0.0 --path TNS_App"
#         output = runAUT(command + " < y_key.txt")
#         assert ("You are going to downgrade to android runtime v.1.0.0. Are you sure?" in output)
#         assert ("Successfully updated to version  1.0.0" in output)

        os.system(tnsPath + " platform update android@1.1.0 --path TNS_App < y_key.txt")
        sleep(10)
        
        output = runAUT("cat TNS_App/package.json")
        assert ("\"version\": \"1.1.0\"" in output)
        Build(platform="android", path="TNS_App")

    def test_210_Platform_Update_Android_PlatformNotAdded(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " platform update android --path TNS_App")
        assert("Copying template files..." in output)
        assert("Project successfully created." in output)
        assert not IsEmpty("TNS_App/platforms/android/build-tools/android-static-binding-generator")

    def test_220_SetSDK(self):
        CreateProject(projName="TNS_App")
        PlatformAdd(platform="android --sdk 19", frameworkPath=androidRuntimePath, path="TNS_App")

        output = runAUT("cat TNS_App/platforms/android/src/main/AndroidManifest.xml ")
        assert ("android:minSdkVersion=\"17\"" in output)      
        assert ("android:targetSdkVersion=\"19\"" in output)

    def test_221_SetSDK_NotInstalled(self):
        CreateProject(projName="TNS_App")
        output = PlatformAdd(platform="android --sdk 29", frameworkPath=androidRuntimePath, path="TNS_App")
        assert ("Support for the selected Android target SDK android-29 is not verified. Your Android app might not work as expected." in output)

        output = runAUT("cat TNS_App/platforms/android/src/main/AndroidManifest.xml")
        assert ("android:minSdkVersion=\"17\"" in output)
        assert ("android:targetSdkVersion=\"29\"/>" in output)

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

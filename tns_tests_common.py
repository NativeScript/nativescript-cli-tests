import os
import platform
import unittest

from helpers._os_lib import CleanupFolder, runAUT, CheckOutput, CheckFilesExists
from helpers._tns_lib import CreateProject, tnsPath, nativescriptPath, \
    AddPlatform, GetAndroidFrameworkPath
from helpers.emulator import StopEmulators, StartEmulator


# This class runs only on all test nodes
class TNSTests_Common(unittest.TestCase):
    
    def setUp(self):
        print "#####"
        print "Cleanup test folders started..."
        CleanupFolder('./folder');
        CleanupFolder('./TNS_Javascript');
        print "Cleanup test folders completed!"
        print "#####"
        
        print self.id()

    def tearDown(self):        
        StopEmulators()

    def test_010_TNSHelp(self):
        command = tnsPath + " help"
        output = runAUT(command)
        CheckOutput(output, 'help_output.txt')
        assert not ("Error" in output)

    def test_011_NativescriptHelp(self):
        command = nativescriptPath + " help"
        output = runAUT(command)
        CheckOutput(output, 'help_output.txt')
        assert not ("Error" in output)
        
    def test_012_CommandHelp(self):
        command = tnsPath + " create --help"
        output = runAUT(command)
        CheckOutput(output, 'create_help_output.txt')
        assert not ("Error" in output)
 
    def test_013_CommandHelp(self):
        command = tnsPath + " create -h"
        output = runAUT(command)
        CheckOutput(output, 'create_help_output.txt')
        assert not ("Error" in output)

    def test_014_CommandHelp(self):
        command = tnsPath + " create ?"
        output = runAUT(command)
        CheckOutput(output, 'create_help_output.txt')
        assert not ("Error" in output)
                       
    def test_020_CreateProject(self):
        projName = "TNS_Javascript"
        CreateProject(projName)
        
        # TODO: Uncomment this after TNS template on Github is OK
        #assert(CheckFilesExists(projName, 'template_javascript_files.txt'))
        
    def test_021_CreateProjectWithPath(self):
        projName = "TNS_Javascript"
        CleanupFolder('./folder');
        CreateProject(projName, 'folder/subfolder/')
        
        # TODO: Uncomment this after TNS template on Github is OK
        # assert(CheckFilesExists('folder/subfolder/' + projName, 'template_javascript_files.txt'))
        
    def test_040_PlatformAdd(self):
        
        self.test_020_CreateProject()
        
        output = AddPlatform(None, GetAndroidFrameworkPath(), "TNS_Javascript")
        assert ("No platform specified. Please specify a platform to add" in output)      
        assert ("$ tns platform add <Platform>" in output)    
        assert ("$ nativescript platform add <Platform>" in output)   
        assert ("$ tns platform add android" in output)     
        assert ("$ tns platform add ios" in output)  
        assert ("$ nativescript platform add android" in output)  
        assert ("$ nativescript platform add ios" in output)    
        assert ("Configures the current project to target the selected platform." in output)
        assert ("In this version of the Telerik NativeScript CLI, you can target iOS and Android, based on your system." in output)  
        assert ("On Windows systems, you can target Android." in output)  
        assert ("On OS X systems, you can target Android and iOS." in output)  
        assert not ("Error" in output) 

    def test_041_PlatformAddAndroid(self):
        
        self.test_020_CreateProject()
        
        output = AddPlatform("android", GetAndroidFrameworkPath(), "TNS_Javascript")
        assert ("Copying template files..." in output)  
        assert ("Updated project.properties" in output)  
        assert ("Updated local.properties" in output)  
        assert ("Project successfully created." in output)
        assert not ("Error" in output) 
        
        command = tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("The project is not prepared for any platform" in output)      
        assert ("Installed platforms:  android" in output)      
        assert not ("Error" in output)   
                 
    def test_050_PlatformRemove(self):

        self.test_020_CreateProject()
        
        command = tnsPath + " platform remove --path TNS_Javascript"
        output = runAUT(command)             
        assert ("No platform specified. Please specify a platform to remove" in output) 
        assert ("$ tns platform remove <Platform>" in output)
        assert ("$ nativescript platform remove <Platform>" in output)
        assert ("$ tns platform remove android" in output)
        assert ("$ tns platform remove ios" in output)
        assert ("$ nativescript platform remove android" in output)
        assert ("$ nativescript platform remove ios" in output)
        assert ("Removes the selected platform from the platforms that the project currently targets." in output)
        assert ("This operation deletes the subdirectory for the selected platform from the platforms directory." in output)
        assert not ("Error" in output) 
                
    def test_051_PlatformRemoveAndroid(self):

        self.test_041_PlatformAddAndroid();
 
        command = tnsPath + " platform remove android --path TNS_Javascript"
        output = runAUT(command)    
        assert not ("Error" in output) 
        
        command = tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Available platforms for this OS:" in output)      
        assert ("android" in output)    
        assert ("No installed platforms found. Use $ tns platform add" in output)    
        assert not ("Error" in output)                   
 
    def test_060_PreparePlatform(self):
           
        self.test_041_PlatformAddAndroid();
                
        command = tnsPath + " prepare --path TNS_Javascript"
        output = runAUT(command)  
        assert ("You need to provide all the required parameters." in output)  
        assert ("$ tns prepare <Platform>" in output)
        assert ("$ nativescript prepare <Platform>" in output)
        assert ("$ tns prepare android" in output)
        assert ("$ tns prepare ios" in output)
        assert ("$ nativescript prepare android" in output)  
        assert ("$ nativescript prepare ios" in output)  
        assert ("Copies common and relevant platform-specific content from the app directory to the subdirectory for the selected target platform" in output)  
        assert ("This lets you build the project with the SDK for the selected platform." in output)  
        assert not ("Error" in output) 
                 
    def test_061_PreparePlatformAndroid(self):
        
        self.test_041_PlatformAddAndroid();
                
        command = tnsPath + " prepare android --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Project successfully prepared" in output)      
        assert not ("Error" in output)                    
 
    def test_063_PreparePlatformThatIsNotAddedToTheProject(self):
        
        self.test_020_CreateProject()       
        
        command = tnsPath + " prepare android --path TNS_Javascript"
        output = runAUT(command) 
        
        assert ("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)    
        assert ("$ tns prepare <Platform>" in output)
        assert ("$ nativescript prepare <Platform>" in output)
        assert ("$ tns prepare android" in output)
        assert ("$ tns prepare ios" in output)
        assert ("$ nativescript prepare android" in output)  
        assert ("$ nativescript prepare ios" in output)  
        assert ("Copies common and relevant platform-specific content from the app directory to the subdirectory for the selected target platform" in output)  
        assert ("This lets you build the project with the SDK for the selected platform." in output) 
        assert not ("Error" in output)     
          
    def test_070_BuildPlatform(self):
        
        self.test_061_PreparePlatformAndroid()
        
        command = tnsPath + " build --path TNS_Javascript"
        output = runAUT(command)   
          
        assert ("You need to provide all the required parameters." in output)    
        assert ("$ tns build <Platform> [--device] [--release]" in output)
        assert ("$ nativescript build <Platform> [--device] [--release]" in output)
        assert ("$ tns build android [--release]" in output)
        assert ("$ tns build ios [--device] [--release]" in output)
        assert ("$ nativescript build android [--release]" in output)  
        assert ("$ nativescript build ios [--device] [--release]" in output)  
        assert ("Builds the project for the selected target platform and produces an application package that you can manually deploy on device or in the native emulator." in output)  
        assert ("Before building for iOS device, verify that you have configured a valid pair of certificate and provisioning profile on your OS X system." in output) 
        assert ("--release - If set, produces a release build. Otherwise, produces a debug build." in output)  
        assert ("--device - This flag is applicable only to iOS. If set, produces an application package that you can deploy on device." in output)  
        assert not ("Error" in output)   
         
    def test_071_BuildPlatformAndroid(self):
        
        self.test_061_PreparePlatformAndroid()
                
        command = tnsPath + " build android --path TNS_Javascript"
        output = runAUT(command)    
        assert ("signing it with a debug key..." in output) 
        assert ("BUILD SUCCESSFUL" in output) 
        assert ("Project successfully built" in output) 
        assert not ("Error" in output)      
 
  
        self.test_061_PreparePlatformAndroid()
 
    def test_080_EmulatePlatform(self):
            
        self.test_061_PreparePlatformAndroid()
                  
        command = tnsPath + " emulate --path TNS_Javascript"
        output = runAUT(command)     
        
        assert ("You need to provide all the required parameters." in output) 
        assert ("$ tns emulate <Platform>" in output) 
        assert ("$ nativescript emulate <Platform>" in output) 
        assert ("$ tns emulate android" in output) 
        assert ("$ tns emulate ios" in output) 
        assert ("$ nativescript emulate android" in output) 
        assert ("$ nativescript emulate ios" in output) 
        assert ("Builds and runs the project in the native emulator for the selected target platform." in output) 
        assert not ("Error" in output) 

    def test_081_EmulatePlatformAndroid(self):
     
        # Start emulator on Linux and Mac 
        # Reason:
        # On Linux and Mac nodes we have no active UI session.
        # CLI start emulator with default params.
        # Emulator started with default params require active UI session.
        
        if 'nt' not in os.name:
            StartEmulator("Api19");
            
        self.test_061_PreparePlatformAndroid()
                   
        command = tnsPath + " emulate android --path TNS_Javascript --timeout 600"
        output = runAUT(command, 600)   
           
        assert ("BUILD SUCCESSFUL" in output) 
        assert ("Project successfully built" in output) 
        
        if 'nt' in os.name:
            assert ("Starting Android emulator with image" in output)    
         
        assert ("installing" in output) 
        assert ("running" in output) 
        assert ("TNS_Javascript-debug.apk through adb" in output) 
        assert not ("Error" in output) 
        
        StopEmulators();
        
    def test_082_EmulatePlatformAndroidOnSpecifiedAvd(self):
     
        # Start emulator on Linux and Mac 
        # Reason:
        # On Linux and Mac nodes we have no active UI session.
        # CLI start emulator with default params.
        # Emulator started with default params require active UI session.
        
        if 'nt' not in os.name:
            StartEmulator("Api19");
             
        self.test_061_PreparePlatformAndroid()
                   
        command = tnsPath + " emulate android --avd Api19 --path TNS_Javascript --timeout 600"
        output = runAUT(command, 600)  
           
        assert ("BUILD SUCCESSFUL" in output) 
        assert ("Project successfully built" in output) 
      
        if 'nt' in os.name:
            assert ("Starting Android emulator with image Api19" in output) 
                    
        assert ("installing" in output) 
        assert ("running" in output) 
        assert ("TNS_Javascript-debug.apk through adb" in output) 
        assert not ("Error" in output) 
        
        command = tnsPath + " emulate android --avd Api19 --path TNS_Javascript --timeout 600"
        output = runAUT(command)   
           
        assert ("BUILD SUCCESSFUL" in output) 
        assert ("Project successfully built" in output) 
      
        assert not ("Starting Android emulator with image" in output) 
                    
        assert ("installing" in output) 
        assert ("running" in output) 
        assert ("TNS_Javascript-debug.apk through adb" in output) 
        assert not ("Error" in output)       
        
        StopEmulators();
         
    def test_090_DeployPlatform(self):
        
        self.test_061_PreparePlatformAndroid()
                
        command = tnsPath + " deploy --path TNS_Javascript"
        output = runAUT(command)  
           
        assert ("You need to provide all the required parameters." in output) 
        assert ("$ tns deploy <Platform> [--device <Device ID>]" in output) 
        assert ("$ nativescript deploy <Platform> [--device <Device ID>]" in output) 
        assert ("$ tns deploy android [--device <Device ID>]" in output) 
        assert ("$ tns deploy ios [--device <Device ID>]" in output) 
        assert ("$ nativescript deploy android [--device <Device ID>]" in output) 
        assert ("$ nativescript deploy ios [--device <Device ID>]" in output) 
        assert ("Builds and deploys the project to a connected physical or virtual device." in output) 
        assert ("<Device ID> is the index or name of the target device as listed by $ tns device." in output) 
        assert ("Before building for iOS device, verify that you have configured a valid pair of certificate and provisioning profile on your OS X system." in output) 
        assert not ("Error" in output) 

    def test_091_DeployPlatformAndroidOnMissingDevice(self):
        
        self.test_061_PreparePlatformAndroid()
                
        command = tnsPath + " deploy android --device fakeDevice --path TNS_Javascript"
        output = runAUT(command)  
        
        assert ("BUILD SUCCESSFUL" in output) 
        assert ("Project successfully built" in output)   
        
        assert ("Cannot resolve the specified connected device by the provided index or identifier." in output) 
        assert ("To list currently connected devices and verify that the specified index or identifier exists, run 'appbuilder device'." in output)      
        # TODO: Update assert message after https://github.com/NativeScript/nativescript-cli/issues/112 is fixed
        
        assert not ("Error" in output) 
        
    def test_092_DeployPlatformAndroidWithRunningDevice(self):
        
        StartEmulator("Api17");
                
        self.test_061_PreparePlatformAndroid()
                
        command = tnsPath + " deploy android --path TNS_Javascript"
        output = runAUT(command)  
        
        assert ("BUILD SUCCESSFUL" in output) 
        assert ("Project successfully built" in output)   
        
        assert ("TNS_Javascript-debug.apk" in output) 
        assert ("Successfully deployed on device with identifier" in output)      
              
        assert not ("Error" in output) 
        
    def test_093_DeployPlatformAndroidWithoutRunningDevice(self):        
        
        self.test_061_PreparePlatformAndroid()
        
        command = tnsPath + " deploy android --path TNS_Javascript"
        output = runAUT(command)  
        
        if 'Darwin' in platform.platform():
            assert ("BUILD SUCCESSFUL" in output) 
            assert ("Project successfully built" in output) 
            assert ("Successfully deployed on device with identifier" in output) 
        else:
            assert ("BUILD SUCCESSFUL" in output) 
            assert ("Project successfully built" in output)   
            assert ("TNS_Javascript-debug.apk" in output) 
            assert ("Cannot find connected devices." in output)      
            assert ("Reconnect any connected devices" in output) 
            assert ("and run this command again" in output)      
  

    def test_100_RunPlatform(self):
        
        self.test_061_PreparePlatformAndroid()
                
        command = tnsPath + " run --path TNS_Javascript"
        output = runAUT(command)     
        
        assert ("You need to provide all the required parameters." in output) 
        assert ("tns run <Platform> [--device <Device ID>] [--emulator]" in output)  
        assert ("nativescript run <Platform> [--device <Device ID>] [--emulator]" in output)  
        assert ("Runs your project on a connected device or in the native emulator, if configured. This is shorthand for prepare, build, and deploy." in output)
        assert ("Before building for the Android emulator, verify that you have met the following requirements." in output)
        assert ("You have added the file paths to the following directories from the Android SDK to your PATH environment variable." in output)
        assert ("You have created at least one device with the Android Virtual Device manager." in output)
        assert ("Before building for the iOS simulator, verify that you have installed the ios-sim npm package." in output)
        assert ("Before building for iOS device, verify that you have configured a valid pair of certificate and provisioning profile on your OS X system." in output)
        assert ("--device - Specifies a connected device on which to run the app." in output) 
        assert ("--emulator - If set, runs the app in the native emulator for the target platform, if configured." in output)   
                                       
        assert not ("Error" in output) 
         
    def test_101_RunPlatformAndroidOnMissingDevice(self):
        
        self.test_061_PreparePlatformAndroid()
        
        command = tnsPath + " run android --device fakeDevice --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Cannot resolve the specified connected device by the provided index or identifier." in output)
        assert ("To list currently connected devices and verify that the specified index or identifier exists, run 'appbuilder device'." in output)                    
        # TODO: Update assert message after https://github.com/NativeScript/nativescript-cli/issues/112 is fixed
    
    def test_102_RunPlatformAndroidOnEmulator(self):
        
        StartEmulator("Api19");
         
        self.test_061_PreparePlatformAndroid()
         
        if 'nt' not in os.name:
            command = tnsPath + " run android --emulator --path TNS_Javascript"
        else:
            command = tnsPath + " run android --device emulator-5554 --path TNS_Javascript --timeout 600"
        
        output = runAUT(command, 600)     
        assert ("BUILD SUCCESSFUL" in output)

        if 'nt' not in os.name:
            assert ("installing" in output)     
            assert ("running" in output)     
            assert ("TNS_Javascript-debug.apk through adb" in output) 
        else:
            assert ("Successfully deployed on device with identifier 'emulator-5554'" in output)  
                    
        StopEmulators();
                                                   
    def test_110_ListDevices(self):
        
        StartEmulator("Api19");
                
        command = tnsPath + " device"
        output = runAUT(command)     
        
        assert ("Android emulator-" in output) 
        assert not ("Reconnect any connected devices, verify that your system recognizes them, and run this command again" in output)     
        assert not ("Error" in output)

    def test_120_FeatureUsageTracking(self):
        
        command = tnsPath + " feature-usage-tracking"
        output = runAUT(command)   
        assert ("Feature usage tracking is disabled" in output)    
        assert not ("Error" in output)    

    def test_121_FeatureUsageTrackingEnable(self):
        
        command = tnsPath + " feature-usage-tracking enable"
        output = runAUT(command)   
        assert ("Feature usage tracking is now enabled." in output)    
        assert not ("Error" in output)  
        
        command = tnsPath + " feature-usage-tracking status"
        output = runAUT(command)   
        assert ("Feature usage tracking is enabled." in output)    
        assert not ("Error" in output)  
 
    def test_122_FeatureUsageTrackingDisable(self):
        
        command = tnsPath + " feature-usage-tracking disable"
        output = runAUT(command)   
        assert ("Feature usage tracking is now disabled." in output)    
        assert not ("Error" in output)  
        
        command = tnsPath + " feature-usage-tracking status"
        output = runAUT(command)   
        assert ("Feature usage tracking is disabled." in output)    
        assert not ("Error" in output) 
         
    def test_123_FeatureUsageTrackingWithInvalidParameter(self):
        command = tnsPath + " feature-usage-tracking invalidParam"
        output = runAUT(command)   
        assert ("The value 'invalidParam' is not valid. Valid values are 'enable', 'disable' and 'status'." in output)  
        assert ("$ tns feature-usage-tracking [<Command>]" in output)   
        assert ("status - Shows the current configuration for anonymous usage tracking" in output)  
        assert ("enable - Enables anonymous usage statistics tracking." in output)  
        assert ("disable - Disables anonymous usage statistics tracking." in output)  
        assert not ("Error" in output)
        
    def test_200_InvalidCommand(self):
        
        command = tnsPath + " invalidCommand"
        output = runAUT(command)   
        assert ("Unknown command" in output)    
        assert ("Use 'NativeScript help' for help." in output) 
        
    def test_201_InvalidCommand(self):
        
        command = tnsPath + " 4"
        output = runAUT(command)   
        assert ("Unknown command" in output)    
        assert ("Use 'NativeScript help' for help." in output) 
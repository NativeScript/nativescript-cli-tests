import unittest, os

from _os_lib import *
from _tns_lib import *
from helpers._os_lib import CleanupFolder, runAUT, CheckOutput, CheckFilesExists
from helpers._tns_lib import CreateProject


class TNSTests_Common(unittest.TestCase):
    
    tnsPath = os.path.join('node_modules', '.bin', 'tns');
    nativescriptPath = os.path.join('node_modules', '.bin', 'nativescript');
            
    def setUp(self):
        print "#####"
        print "Cleanup test folders started..."
        CleanupFolder('./folder');
        CleanupFolder('./TNS_Javascript');
        print "Cleanup test folders completed!"
        print "#####"
        
        print self.id()

    def tearDown(self):
        pass

    def test_010_TNSHelp(self):
        command = self.tnsPath + " help"
        output = runAUT(command)
        CheckOutput(output, 'help_output.txt')
        assert not ("Error" in output)

    def test_011_NativescriptHelp(self):
        command = self.nativescriptPath + " help"
        output = runAUT(command)
        CheckOutput(output, 'help_output.txt')
        assert not ("Error" in output)
        
    def test_020_CreateProject(self):
        projName = "TNS_Javascript"
        CreateProject(projName)
        assert(CheckFilesExists(projName, 'template_javascript_files.txt'))
        
    def test_021_CreateProjectWithPath(self):
        projName = "TNS_Javascript"
        CleanupFolder('./folder');
        CreateProject(projName, 'folder/subfolder/')
        assert(CheckFilesExists('folder/subfolder/' + projName, 'template_javascript_files.txt'))     
        
    def test_030_PlatformList(self):
        
        self.test_020_CreateProject()
        
        command = self.tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Available platforms for this OS:" in output)      
        assert ("android" in output)    
        assert ("No installed platforms found. Use $ tns platform add" in output)    
        assert not ("Error" in output)  
         
    def test_040_PlatformAdd(self):
        
        self.test_020_CreateProject()
        
        command = self.tnsPath + " platform add --path TNS_Javascript"
        output = runAUT(command)
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
        
        command = self.tnsPath + " platform add android --path TNS_Javascript"
        output = runAUT(command)     
        assert ("Copying template files..." in output)  
        assert ("Updated project.properties" in output)  
        assert ("Updated local.properties" in output)  
        assert ("Project successfully created." in output)
        assert not ("Error" in output) 
        
        command = self.tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("The project is not prepared for any platform" in output)      
        assert ("Installed platforms:" in output)      
        assert ("android" in output)    
        assert not ("Error" in output)                    
 
    def test_050_PlatformRemove(self):

        self.test_020_CreateProject()
        
        command = self.tnsPath + " platform remove --path TNS_Javascript"
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
 
        command = self.tnsPath + " platform remove android --path TNS_Javascript"
        output = runAUT(command)    
        assert not ("Error" in output) 
        
        command = self.tnsPath + " platform list --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Available platforms for this OS:" in output)      
        assert ("android" in output)    
        assert ("No installed platforms found. Use $ tns platform add" in output)    
        assert not ("Error" in output)                   
 
    def test_060_PreparePlatform(self):
           
        self.test_041_PlatformAddAndroid();
                
        command = self.tnsPath + " prepare --path TNS_Javascript"
        output = runAUT(command)  
        assert ("No platform specified." in output)  
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
                
        command = self.tnsPath + " prepare android --path TNS_Javascript"
        output = runAUT(command) 
        assert ("Project successfully prepared" in output)      
        assert not ("Error" in output)                    
 
    def test_063_PreparePlatformThatIsNotAddedToTheProject(self):
        
        self.test_020_CreateProject()       
        
        command = self.tnsPath + " prepare android --path TNS_Javascript"
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
        
        command = self.tnsPath + " build --path TNS_Javascript"
        output = runAUT(command)   
          
        assert ("No platform specified." in output)    
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
                
        command = self.tnsPath + " build android --path TNS_Javascript"
        output = runAUT(command)     
        assert ("BUILD SUCCESSFUL" in output) 
        assert not ("Error" in output)                    
 
    def test_080_EmulatePlatform(self):
  
        self.test_020_CreateProject()
                
        command = self.tnsPath + " emulate --path TNS_Javascript"
        output = runAUT(command)     
        
        assert ("No platform specified." in output) 
        assert ("$ tns emulate <Platform>" in output) 
        assert ("$ nativescript emulate <Platform>" in output) 
        assert ("$ tns emulate android" in output) 
        assert ("$ tns emulate ios" in output) 
        assert ("$ nativescript emulate android" in output) 
        assert ("$ nativescript emulate ios" in output) 
        assert ("Builds and runs the project in the native emulator for the selected target platform." in output) 
        assert not ("Error" in output) 
         
    def test_090_DeployPlatform(self):
        
        self.test_061_PreparePlatformAndroid()
                
        command = self.tnsPath + " deploy --path TNS_Javascript"
        output = runAUT(command)  
           
        assert ("No platform specified." in output) 
        assert ("$ tns deploy <Platform> [--device <Device ID>]" in output) 
        assert ("$ nativescript deploy <Platform> [--device <Device ID>]" in output) 
        assert ("$ tns deploy android [--device <Device ID>]" in output) 
        assert ("$ tns deploy ios [--device <Device ID>]" in output) 
        assert ("$ nativescript deploy android [--device <Device ID>]" in output) 
        assert ("$ nativescript deploy ios [--device <Device ID>]" in output) 
        assert ("Builds and deploys the project to a connected physical or virtual device" in output) 
        assert ("<Device ID> is the index or name of the target device as listed by $ tns device" in output) 
        assert ("Before building for iOS device, verify that you have configured a valid pair of certificate and provisioning profile on your OS X system." in output) 
        assert not ("Error" in output) 
         
    def test_110_ListDevices(self):
        
        command = self.tnsPath + " device"
        output = runAUT(command)     
        assert not ("Error" in output) 
        # TODO: Add more asserts once we have final QA environment
        
    def test_120_FeatureUsageTracking(self):
        
        command = self.tnsPath + " feature-usage-tracking"
        output = runAUT(command)   
        assert ("Feature usage tracking is disabled" in output)    
        assert not ("Error" in output)    

    def test_121_FeatureUsageTrackingEnable(self):
        
        command = self.tnsPath + " feature-usage-tracking enable"
        output = runAUT(command)   
        assert ("Feature usage tracking is now enabled." in output)    
        assert not ("Error" in output)  
        
        command = self.tnsPath + " feature-usage-tracking status"
        output = runAUT(command)   
        assert ("Feature usage tracking is enabled." in output)    
        assert not ("Error" in output)  
 
    def test_122_FeatureUsageTrackingDisable(self):
        
        command = self.tnsPath + " feature-usage-tracking disable"
        output = runAUT(command)   
        assert ("Feature usage tracking is now disabled." in output)    
        assert not ("Error" in output)  
        
        command = self.tnsPath + " feature-usage-tracking status"
        output = runAUT(command)   
        assert ("Feature usage tracking is disabled." in output)    
        assert not ("Error" in output) 
         
    def test_123_FeatureUsageTrackingWithInvalidParameter(self):
        command = self.tnsPath + " feature-usage-tracking invalidParam"
        output = runAUT(command)   
        assert ("Invalid parameter" in output)  
        assert ("$ tns feature-usage-tracking [<Command>]" in output)   
        assert ("status - Shows the current configuration for anonymous usage tracking" in output)  
        assert ("enable - Enables anonymous usage statistics tracking." in output)  
        assert ("disable - Disables anonymous usage statistics tracking." in output)  
        assert not ("Error" in output)   
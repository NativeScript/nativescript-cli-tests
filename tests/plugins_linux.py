import os
import platform
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import CreateProjectAndAddPlatform, androidRuntimePath, \
    tnsPath, CreateProject


class Plugins_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_001_PluginAdd_Before_PlatformAdd_Android(self):
        CreateProject(projName="TNS_App");        
        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        if 'Windows' not in platform.platform():
            assert ("TNS_App/node_modules/tns-plugin" in output)
        assert ("Successfully installed plugin tns-plugin" in output)
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("dependencies" in output)
        assert ("tns-plugin" in output)
        
    def test_002_PluginAdd_After_PlatformAdd_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)    
        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App");
        if 'Windows' not in platform.platform():
            assert ("TNS_App/node_modules/tns-plugin" in output)
        assert ("Successfully installed plugin tns-plugin" in output)
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("dependencies" in output)
        assert ("tns-plugin" in output)
    
    def test_003_PluginAdd_InsideProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)     
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))   
        output = runAUT(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(currentDir);
        if 'Windows' not in platform.platform():
            assert ("node_modules/tns-plugin" in output)
        assert ("Successfully installed plugin tns-plugin" in output)
        assert FileExists("TNS_App/node_modules/tns-plugin/index.js")
        assert FileExists("TNS_App/node_modules/tns-plugin/package.json")
        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("dependencies" in output)
        assert ("tns-plugin" in output)

    def test_100_BuildAppWithPluginAddedInsideProject(self):
        
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir,"TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " plugin add tns-plugin")
        os.chdir(currentDir);
        assert ("Successfully installed plugin tns-plugin" in output)
        
        output = runAUT(tnsPath + " build android --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Creating TNSApp-debug-unaligned.apk and signing it with a debug key..." in output)  
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)  
        assert not ("ERROR" in output)   
        assert not ("malformed" in output)            
        assert FileExists("TNS_App/platforms/android/bin/TNSApp-debug.apk")
        assert FileExists("TNS_App/platforms/android/assets/app/tns_modules/tns-plugin/index.js")
 
    def test_300_BuildAppWithPluginAddedOutsideProject(self):
        
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)

        output = runAUT(tnsPath + " plugin add tns-plugin --path TNS_App")
        assert ("Successfully installed plugin tns-plugin" in output)
        
        output = runAUT(tnsPath + " build android --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Creating TNSApp-debug-unaligned.apk and signing it with a debug key..." in output)  
        assert ("BUILD SUCCESSFUL" in output)
        assert ("Project successfully built" in output)  
        assert not ("ERROR" in output)   
        assert not ("malformed" in output)            
        assert FileExists("TNS_App/platforms/android/bin/TNSApp-debug.apk")
        assert FileExists("TNS_App/platforms/android/assets/app/tns_modules/tns-plugin/index.js")

    @unittest.skip("This test breaks the xml parser.")
    def test_400_PluginAdd_NotExistingPlugin(self):
        CreateProject(projName="TNS_App");        
        output = runAUT(tnsPath + " plugin add fakePlugin --path TNS_App")
        assert ("no such package available" in output)

    def test_401_PluginAdd_InvalidPlugin(self):
        CreateProject(projName="TNS_App");        
        output = runAUT(tnsPath + " plugin add wd --path TNS_App")
        assert ("wd is not a valid NativeScript plugin" in output)
        assert ("Verify that the plugin package.json file contains a nativescript key and try again" in output)
        
    def test_403_PluginAdd_PluginNotSupportedOnSpecificPlatform(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)    
        output = runAUT(tnsPath + " plugin add tns-plugin@1.0.2 --path TNS_App");
        assert ("tns-plugin is not supported for android" in output)
        assert ("Successfully installed plugin tns-plugin" in output)

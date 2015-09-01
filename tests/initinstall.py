import fileinput
import os
import platform
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import tnsPath


class InitAndInstall(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_001_Init_Defaults(self):
        
        runAUT("mkdir TNS_App")
        
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))   
        output = runAUT(os.path.join("..", tnsPath) + " init --force")
        os.chdir(currentDir);
        
        assert ("Project successfully initialized" in output)
        assert FileExists("TNS_App/package.json")
        assert not FileExists("TNS_App/app")
        assert not FileExists("TNS_App/platform")

        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("tns-android" in output)
        if 'Darwin' in platform.platform():
            assert ("tns-ios" in output)
        
    def test_002_Init_Path(self):
        output = runAUT(tnsPath + " init --path TNS_App --force")
        assert ("Project successfully initialized" in output)
        assert FileExists("TNS_App/package.json")
        assert not FileExists("TNS_App/app")
        assert not FileExists("TNS_App/platform")

        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TNSApp" in output)
        assert ("tns-android" in output)
        if 'Darwin' in platform.platform():
            assert ("tns-ios" in output)
                
    def test_003_Init_UpdateExistingFile(self):
        self.test_002_Init_Path();
        
        # Modify existing file
        for line in fileinput.input("TNS_App/package.json", inplace = 1): 
            print line.replace("org.nativescript.TNSApp", "org.nativescript.TestApp"),
        output = runAUT("cat TNS_App/package.json")
        assert ("org.nativescript.TestApp" in output)
        
        # Overwrite changes 
        self.test_002_Init_Path();

    def test_004_InstallDefaults(self):
        self.test_002_Init_Path();
        
        output = runAUT(tnsPath + " install --path TNS_App")
        assert ("Project successfully created" in output)
        
        # Not valid for 1.3.0+
        # assert FileExists("TNS_App/platforms/android/build.gradle")
        assert FileExists("TNS_App/platforms/android/build.gradle")
        
        if 'Darwin' in platform.platform():
            assert FileExists("TNS_App/platforms/ios/TNSApp.xcodeproj")

    def test_005_InstallNodeModules(self):
        self.test_002_Init_Path();
        
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))   
        runAUT("npm i gulp --save-dev")
        runAUT("npm i lodash --save")
        os.chdir(currentDir);
        output = runAUT("cat TNS_App/package.json")
        assert ("devDependencies" in output)
        assert ("gulp" in output)
        assert ("lodash" in output)
 
        CleanupFolder('./TNS_App/node_modules');
        assert not FileExists("TNS_App/node_modules")
                
        output = runAUT(tnsPath + " install --path TNS_App")
        assert ("Project successfully created" in output)
        assert FileExists("TNS_App/node_modules/lodash")
        assert FileExists("TNS_App/node_modules/gulp")
        
        # Not valid for 1.3.0+
        # assert FileExists("TNS_App/platforms/android/build.gradle")
        assert FileExists("TNS_App/platforms/android/build.gradle")
        
        if 'Darwin' in platform.platform():
            assert FileExists("TNS_App/platforms/ios/TNSApp.xcodeproj")

    def test_300_InstallNodeModulesIfNodeModulesFodlerExists(self):
        self.test_002_Init_Path();
        
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))   
        runAUT("npm i gulp --save-dev")
        runAUT("npm i lodash --save")

        os.chdir(currentDir);
        output = runAUT("cat TNS_App/package.json")
        assert ("devDependencies" in output)
        assert ("gulp" in output)
        assert ("lodash" in output)
                
        output = runAUT(tnsPath + " install --path TNS_App")
        assert ("Project successfully created" in output)
        assert FileExists("TNS_App/node_modules/lodash")
        assert FileExists("TNS_App/node_modules/gulp")
        assert FileExists("TNS_App/platforms/android/build.gradle")
        if 'Darwin' in platform.platform():
            assert FileExists("TNS_App/platforms/ios/TNSApp.xcodeproj")
        
    def test_301_InstallAndPrepare(self):
        self.test_002_Init_Path();
        
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))   
        runAUT("npm i gulp --save-dev")
        runAUT("npm i lodash --save")

        os.chdir(currentDir);
        runAUT("cp -R template-hello-world TNS_App/app")
        output = runAUT("cat TNS_App/package.json")
        assert ("devDependencies" in output)
        assert ("gulp" in output)
        assert ("lodash" in output)
                
        output = runAUT(tnsPath + " install --path TNS_App")
        assert ("Project successfully created" in output)
        assert FileExists("TNS_App/node_modules/lodash")
        assert FileExists("TNS_App/node_modules/gulp")
        assert FileExists("TNS_App/platforms/android/build.gradle")
        
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert ("Project successfully prepared" in output)        
        
        assert FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/lodash")
        assert not FileExists("TNS_App/platforms/android/src/main/assets/app/tns_modules/gulp")

        if 'Darwin' in platform.platform():
            assert FileExists("TNS_App/platforms/ios/TNSApp.xcodeproj")                    
            output = runAUT(tnsPath + " prepare ios --path TNS_App")
            assert ("Project successfully prepared" in output)
            assert FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/lodash")
            assert not FileExists("TNS_App/platforms/ios/TNSApp/app/tns_modules/gulp")                 
                                    
    def test_400_Install_InNotExistingFolder(self):
        output = runAUT(tnsPath + " install --path TNS_App")
        assert ("No project found" in output)
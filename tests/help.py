import platform
import unittest

from helpers._os_lib import runAUT, CheckOutput
from helpers._tns_lib import tnsPath, nativescriptPath


class Help(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):        
        pass

    def test_010_TNSHelp(self):
        output = runAUT(tnsPath + " help")
        assert CheckOutput(output, 'help_output.txt')
        assert not ("error" in output)
        
    def test_011_NativescriptHelp(self):
        output = runAUT(nativescriptPath + " help")
        assert CheckOutput(output, 'help_output.txt')
        assert not ("error" in output)
    
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/249")    
    def test_012_TNSHelp(self):
        output = runAUT(tnsPath + " -help")
        assert CheckOutput(output, 'help_output.txt')
        assert not ("error" in output)
        
    def test_013_TNSHelp(self):
        output = runAUT(tnsPath + " --help")
        assert CheckOutput(output, 'help_output.txt')
        assert not ("error" in output)
        
    def test_014_TNSHelp(self):
        output = runAUT(tnsPath + " -h")
        assert CheckOutput(output, 'help_output.txt')
        assert not ("error" in output)
        
    def test_015_TNSHelp(self):
        output = runAUT(tnsPath + " /?")
        assert CheckOutput(output, 'help_output.txt')
        assert not ("error" in output)
        
    def test_020_TNSHelp_Create(self):
        output = runAUT(tnsPath + " create --help")
        assert CheckOutput(output, 'create_help_output.txt')
        assert not ("error" in output)
 
    def test_021_TNSHelp_Create(self):
        output = runAUT(tnsPath + " create -h")
        assert CheckOutput(output, 'create_help_output.txt')
        assert not ("error" in output)

    def test_022_TNSHelp_Create(self):
        output = runAUT(tnsPath + " create ?")
        assert CheckOutput(output, 'create_help_output.txt')
        assert not ("error" in output)
        
    def test_030_TNSHelp_Platform(self):
        output = runAUT(tnsPath + " platform -h")
        assert CheckOutput(output, 'platform_help_output.txt')
        assert not ("error" in output)
        
    def test_031_TNSHelp_Platform_Add(self):
        output = runAUT(tnsPath + " platform add -h")
        assert CheckOutput(output, 'platform_add_help_output.txt')
        assert not ("error" in output)

    def test_032_TNSHelp_Platform_AddAndroid(self):
        output = runAUT(tnsPath + " platform add android -h")
        assert CheckOutput(output, 'platform_add_help_output.txt')
                        
    def test_040_TNSHelp_Prepare(self):
        output = runAUT(tnsPath + " prepare -h")
        assert CheckOutput(output, 'prepare_help_output.txt')
        assert not ("error" in output)
        
    def test_050_TNSHelp_Build(self):
        output = runAUT(tnsPath + " build -h")
        assert CheckOutput(output, 'build_help_output.txt')
        assert not ("error" in output)

    def test_051_TNSHelp_Build_Android(self):
        output = runAUT(tnsPath + " build android -h")
        assert CheckOutput(output, 'buildandroid_help_output.txt')
        assert not ("error" in output)

    def test_052_TNSHelp_Build_iOS(self):
        output = runAUT(tnsPath + " build ios -h")
        assert CheckOutput(output, 'buildios_help_output.txt')
        assert not ("error" in output)
                        
    def test_060_TNSHelp_Deploy(self):
        output = runAUT(tnsPath + " deploy -h")
        assert CheckOutput(output, 'deploy_help_output.txt')
        assert not ("error" in output)
        
    def test_070_TNSHelp_Emulate(self):
        output = runAUT(tnsPath + " emulate -h")
        assert CheckOutput(output, 'emulate_help_output.txt')
        assert not ("error" in output)

    def test_071_TNSHelp_Emulate_Android(self):
        output = runAUT(tnsPath + " emulate android -h")
        if 'Darwin' in platform.platform():
            assert CheckOutput(output, 'emulate_android_help_osx_output.txt')
        else:
            assert CheckOutput(output, 'emulate_android_help_output.txt')
                                
    def test_080_TNSHelp_Run(self):
        output = runAUT(tnsPath + " run -h")
        assert CheckOutput(output, 'run_help_output.txt')
        assert not ("error" in output)
        
    def test_090_TNSHelp_Device(self):
        output = runAUT(tnsPath + " device -h")
        assert CheckOutput(output, 'device_help_output.txt')
        assert not ("error" in output)

    def test_091_TNSHelp_Device_Log(self):
        output = runAUT(tnsPath + " device log -h")
        assert CheckOutput(output, 'devicelog_help_output.txt')
        assert not ("error" in output)

    def test_092_TNSHelp_Device_ListApplications(self):
        output = runAUT(tnsPath + " device list-applications -h")
        assert CheckOutput(output, 'devicelist_help_output.txt')
        assert not ("error" in output)
        
    def test_093_TNSHelp_Device_Run(self):
        output = runAUT(tnsPath + " device run -h")
        assert CheckOutput(output, 'devicerun_help_output.txt')
        assert not ("error" in output)
                
    def test_100_TNSHelp_Debug(self):
        output = runAUT(tnsPath + " debug -h")
        assert CheckOutput(output, 'debug_help_output.txt')
        assert not ("error" in output)
                                
    def test_110_TNSHelp_FeatureUsageTracking(self):
        output = runAUT(tnsPath + " feature-usage-tracking -h")
        assert CheckOutput(output, 'feature_help_output.txt')
        assert not ("error" in output)
        
    def test_400_TNSHelp_InvalidCommand(self):        
        output = runAUT(tnsPath + " invalidCommand")   
        assert ("Unknown command 'invalidcommand'. Use 'tns help' for help." in output)    
        
    def test_401_TNSHelp_InvalidCommand(self):        
        output = runAUT(tnsPath + " 4")   
        assert ("Unknown command '4'. Use 'tns help' for help." in output)
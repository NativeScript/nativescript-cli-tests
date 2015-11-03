import platform
import unittest

from helpers._os_lib import runAUT, CheckOutput
from helpers._tns_lib import tnsPath, nativescriptPath

# pylint: disable=R0201, C0111


class Help(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_TNSHelp(self):
        output = runAUT(tnsPath + " help")
        assert CheckOutput(output, 'help_output.txt')
        assert not "error" in output

    def test_002_NativescriptHelp(self):
        output = runAUT(nativescriptPath + " help")
        assert CheckOutput(output, 'help_output.txt')
        assert not "error" in output

    @unittest.skip(
        "Skipped because of https://github.com/NativeScript/nativescript-cli/issues/249")
    def test_003_TNSHelp(self):
        output = runAUT(tnsPath + " -help")
        assert CheckOutput(output, 'help_output.txt')
        assert not "error" in output

    def test_004_TNSHelp(self):
        output = runAUT(tnsPath + " --help")
        assert CheckOutput(output, 'help_output.txt')
        assert not "error" in output

    def test_005_TNSHelp(self):
        output = runAUT(tnsPath + " -h")
        assert CheckOutput(output, 'help_output.txt')
        assert not "error" in output

    def test_006_TNSHelp(self):
        output = runAUT(tnsPath + " /?")
        assert CheckOutput(output, 'help_output.txt')
        assert not "error" in output

    def test_200_TNSHelp_Create(self):
        output = runAUT(tnsPath + " create --help")
        assert CheckOutput(output, 'create_help_output.txt')
        assert not "error" in output

    def test_201_TNSHelp_Create(self):
        output = runAUT(tnsPath + " create -h")
        assert CheckOutput(output, 'create_help_output.txt')
        assert not "error" in output

    def test_202_TNSHelp_Create(self):
        output = runAUT(tnsPath + " create ?")
        assert CheckOutput(output, 'create_help_output.txt')
        assert not "error" in output

    def test_203_TNSHelp_Platform(self):
        output = runAUT(tnsPath + " platform -h")
        assert CheckOutput(output, 'platform_help_output.txt')
        assert not "error" in output

    def test_204_TNSHelp_Platform_Add(self):
        output = runAUT(tnsPath + " platform add -h")
        assert CheckOutput(output, 'platform_add_help_output.txt')
        assert not "error" in output

    def test_205_TNSHelp_Platform_AddAndroid(self):
        output = runAUT(tnsPath + " platform add android -h")
        assert CheckOutput(output, 'platform_add_help_output.txt')

    def test_206_TNSHelp_Prepare(self):
        output = runAUT(tnsPath + " prepare -h")
        assert CheckOutput(output, 'prepare_help_output.txt')
        assert not "error" in output

    def test_207_TNSHelp_Build(self):
        output = runAUT(tnsPath + " build -h")
        assert CheckOutput(output, 'build_help_output.txt')
        assert not "error" in output

    def test_208_TNSHelp_Build_Android(self):
        output = runAUT(tnsPath + " build android -h")
        assert CheckOutput(output, 'buildandroid_help_output.txt')
        assert not "error" in output

    def test_209_TNSHelp_Build_iOS(self):
        output = runAUT(tnsPath + " build ios -h")
        assert CheckOutput(output, 'buildios_help_output.txt')
        assert not "error" in output

    def test_210_TNSHelp_Deploy(self):
        output = runAUT(tnsPath + " deploy -h")
        assert CheckOutput(output, 'deploy_help_output.txt')
        assert not "error" in output

    def test_211_TNSHelp_Emulate(self):
        output = runAUT(tnsPath + " emulate -h")
        assert CheckOutput(output, 'emulate_help_output.txt')
        assert not "error" in output

    def test_212_TNSHelp_Emulate_Android(self):
        output = runAUT(tnsPath + " emulate android -h")
        if 'Darwin' in platform.platform():
            assert CheckOutput(output, 'emulate_android_help_osx_output.txt')
        else:
            assert CheckOutput(output, 'emulate_android_help_output.txt')

    def test_213_TNSHelp_Run(self):
        output = runAUT(tnsPath + " run -h")
        assert CheckOutput(output, 'run_help_output.txt')
        assert not "error" in output

    def test_214_TNSHelp_Device(self):
        output = runAUT(tnsPath + " device -h")
        assert CheckOutput(output, 'device_help_output.txt')
        assert not "error" in output

    def test_215_TNSHelp_Device_Log(self):
        output = runAUT(tnsPath + " device log -h")
        assert CheckOutput(output, 'devicelog_help_output.txt')
        assert not "error" in output

    def test_216_TNSHelp_Device_ListApplications(self):
        output = runAUT(tnsPath + " device list-applications -h")
        assert CheckOutput(output, 'devicelist_help_output.txt')
        assert not "error" in output

    def test_217_TNSHelp_Device_Run(self):
        output = runAUT(tnsPath + " device run -h")
        assert CheckOutput(output, 'devicerun_help_output.txt')
        assert not "error" in output

    def test_218_TNSHelp_Debug(self):
        output = runAUT(tnsPath + " debug -h")
        assert CheckOutput(output, 'debug_help_output.txt')
        assert not "error" in output

    def test_219_TNSHelp_DebugAndroid(self):
        output = runAUT(tnsPath + " debug android -h")
        assert CheckOutput(output, 'debug_android_help_output.txt')
        assert not "error" in output

    def test_220_TNSHelp_DebugIOS(self):
        output = runAUT(tnsPath + " debug ios -h")
        assert CheckOutput(output, 'debug_ios_help_output.txt')
        assert not "error" in output

    def test_221_TNSHelp_FeatureUsageTracking(self):
        output = runAUT(tnsPath + " feature-usage-tracking -h")
        assert CheckOutput(output, 'feature_help_output.txt')
        assert not "error" in output

    def test_400_TNSHelp_InvalidCommand(self):
        output = runAUT(tnsPath + " invalidCommand")
        assert "Unknown command 'invalidcommand'. Use 'tns help' for help." in output

    def test_401_TNSHelp_InvalidCommand(self):
        output = runAUT(tnsPath + " 4")
        assert "Unknown command '4'. Use 'tns help' for help." in output

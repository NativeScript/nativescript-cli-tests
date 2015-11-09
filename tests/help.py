'''
Test for help command
'''
import platform
import unittest

from helpers._os_lib import run_aut, check_output
from helpers._tns_lib import TNSPATH, NPATH

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class Help(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_help(self):
        output = run_aut(TNSPATH + " help")
        assert check_output(output, 'help_output.txt')
        assert not "error" in output

    def test_002_nativescript_help(self):
        output = run_aut(NPATH + " help")
        assert check_output(output, 'help_output.txt')
        assert not "error" in output

    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/249")
    def test_003_help(self):
        output = run_aut(TNSPATH + " -help")
        assert check_output(output, 'help_output.txt')
        assert not "error" in output

    def test_004_help(self):
        output = run_aut(TNSPATH + " --help")
        assert check_output(output, 'help_output.txt')
        assert not "error" in output

    def test_005_help(self):
        output = run_aut(TNSPATH + " -h")
        assert check_output(output, 'help_output.txt')
        assert not "error" in output

    def test_006_help(self):
        output = run_aut(TNSPATH + " /?")
        assert check_output(output, 'help_output.txt')
        assert not "error" in output

    def test_200_help_create(self):
        output = run_aut(TNSPATH + " create --help")
        assert check_output(output, 'create_help_output.txt')
        assert not "error" in output

    def test_201_help_create(self):
        output = run_aut(TNSPATH + " create -h")
        assert check_output(output, 'create_help_output.txt')
        assert not "error" in output

    def test_202_help_create(self):
        output = run_aut(TNSPATH + " create ?")
        assert check_output(output, 'create_help_output.txt')
        assert not "error" in output

    def test_203_help_platform(self):
        output = run_aut(TNSPATH + " platform -h")
        assert check_output(output, 'platform_help_output.txt')
        assert not "error" in output

    def test_204_help_platform_add(self):
        output = run_aut(TNSPATH + " platform add -h")
        assert check_output(output, 'platform_add_help_output.txt')
        assert not "error" in output

    def test_205_help_platform_add_android(self):
        output = run_aut(TNSPATH + " platform add android -h")
        assert check_output(output, 'platform_add_help_output.txt')

    def test_206_help_prepare(self):
        output = run_aut(TNSPATH + " prepare -h")
        assert check_output(output, 'prepare_help_output.txt')
        assert not "error" in output

    def test_207_help_build(self):
        output = run_aut(TNSPATH + " build -h")
        assert check_output(output, 'build_help_output.txt')
        assert not "error" in output

    def test_208_help_build_android(self):
        output = run_aut(TNSPATH + " build android -h")
        assert check_output(output, 'buildandroid_help_output.txt')
        assert not "error" in output

    def test_209_help_build_ios(self):
        output = run_aut(TNSPATH + " build ios -h")
        assert check_output(output, 'buildios_help_output.txt')
        assert not "error" in output

    def test_210_help_deploy(self):
        output = run_aut(TNSPATH + " deploy -h")
        assert check_output(output, 'deploy_help_output.txt')
        assert not "error" in output

    def test_211_help_emulate(self):
        output = run_aut(TNSPATH + " emulate -h")
        assert check_output(output, 'emulate_help_output.txt')
        assert not "error" in output

    def test_212_help_emulate_android(self):
        output = run_aut(TNSPATH + " emulate android -h")
        if 'Darwin' in platform.platform():
            assert check_output(output, 'emulate_android_help_osx_output.txt')
        else:
            assert check_output(output, 'emulate_android_help_output.txt')

    def test_213_help_run(self):
        output = run_aut(TNSPATH + " run -h")
        assert check_output(output, 'run_help_output.txt')
        assert not "error" in output

    def test_214_help_device(self):
        output = run_aut(TNSPATH + " device -h")
        assert check_output(output, 'device_help_output.txt')
        assert not "error" in output

    def test_215_help_device_Log(self):
        output = run_aut(TNSPATH + " device log -h")
        assert check_output(output, 'devicelog_help_output.txt')
        assert not "error" in output

    def test_216_help_device_list_applications(self):
        output = run_aut(TNSPATH + " device list-applications -h")
        assert check_output(output, 'devicelist_help_output.txt')
        assert not "error" in output

    def test_217_help_device_run(self):
        output = run_aut(TNSPATH + " device run -h")
        assert check_output(output, 'devicerun_help_output.txt')
        assert not "error" in output

    def test_218_help_debug(self):
        output = run_aut(TNSPATH + " debug -h")
        assert check_output(output, 'debug_help_output.txt')
        assert not "error" in output

    def test_219_help_debug_android(self):
        output = run_aut(TNSPATH + " debug android -h")
        assert check_output(output, 'debug_android_help_output.txt')
        assert not "error" in output

    def test_220_help_debug_ios(self):
        output = run_aut(TNSPATH + " debug ios -h")
        assert check_output(output, 'debug_ios_help_output.txt')
        assert not "error" in output

    def test_221_help_feature_usage_tracking(self):
        output = run_aut(TNSPATH + " feature-usage-tracking -h")
        assert check_output(output, 'feature_help_output.txt')
        assert not "error" in output

    def test_400_help_invalid_command(self):
        output = run_aut(TNSPATH + " invalidCommand")
        assert "Unknown command 'invalidcommand'. Use 'tns help' for help." in output

    def test_401_help_invalid_command(self):
        output = run_aut(TNSPATH + " 4")
        assert "Unknown command '4'. Use 'tns help' for help." in output

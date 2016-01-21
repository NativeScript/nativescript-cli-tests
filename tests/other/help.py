"""
Test for help command
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType


@unittest.skip("Skipped because tests are out of date.")
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
        output = run(TNS_PATH + " help")
        assert File.string_contains_file_content(output, 'help_output.txt')
        assert "error" not in output

    def test_002_nativescript_help(self):
        output = run(TNS_PATH + " help")
        assert File.string_contains_file_content(output, 'help_output.txt')
        assert "error" not in output

    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/249")
    def test_003_help(self):
        output = run(TNS_PATH + " -help")
        assert File.string_contains_file_content(output, 'help_output.txt')
        assert "error" not in output

    def test_004_help(self):
        output = run(TNS_PATH + " --help")
        assert File.string_contains_file_content(output, 'help_output.txt')
        assert "error" not in output

    def test_005_help(self):
        output = run(TNS_PATH + " -h")
        assert File.string_contains_file_content(output, 'help_output.txt')
        assert "error" not in output

    def test_006_help(self):
        output = run(TNS_PATH + " /?")
        assert File.string_contains_file_content(output, 'help_output.txt')
        assert "error" not in output

    def test_200_help_create(self):
        output = run(TNS_PATH + " create --help")
        assert File.string_contains_file_content(output, 'create_help_output.txt')
        assert "error" not in output

    def test_201_help_create(self):
        output = run(TNS_PATH + " create -h")
        assert File.string_contains_file_content(output, 'create_help_output.txt')
        assert "error" not in output

    def test_202_help_create(self):
        output = run(TNS_PATH + " create ?")
        assert File.string_contains_file_content(output, 'create_help_output.txt')
        assert "error" not in output

    def test_203_help_platform(self):
        output = run(TNS_PATH + " platform -h")
        assert File.string_contains_file_content(output, 'platform_help_output.txt')
        assert "error" not in output

    def test_204_help_platform_add(self):
        output = run(TNS_PATH + " platform add -h")
        assert File.string_contains_file_content(output, 'platform_add_help_output.txt')
        assert "error" not in output

    def test_205_help_platform_add_android(self):
        output = run(TNS_PATH + " platform add android -h")
        assert File.string_contains_file_content(output, 'platform_add_help_output.txt')

    def test_206_help_prepare(self):
        output = run(TNS_PATH + " prepare -h")
        assert File.string_contains_file_content(output, 'prepare_help_output.txt')
        assert "error" not in output

    def test_207_help_build(self):
        output = run(TNS_PATH + " build -h")
        assert File.string_contains_file_content(output, 'build_help_output.txt')
        assert "error" not in output

    def test_208_help_build_android(self):
        output = run(TNS_PATH + " build android -h")
        assert File.string_contains_file_content(output, 'buildandroid_help_output.txt')
        assert "error" not in output

    def test_209_help_build_ios(self):
        output = run(TNS_PATH + " build ios -h")
        assert File.string_contains_file_content(output, 'buildios_help_output.txt')
        assert "error" not in output

    def test_210_help_deploy(self):
        output = run(TNS_PATH + " deploy -h")
        assert File.string_contains_file_content(output, 'deploy_help_output.txt')
        assert "error" not in output

    def test_211_help_emulate(self):
        output = run(TNS_PATH + " emulate -h")
        assert File.string_contains_file_content(output, 'emulate_help_output.txt')
        assert "error" not in output

    def test_212_help_emulate_android(self):
        output = run(TNS_PATH + " emulate android -h")
        if CURRENT_OS == OSType.OSX:
            assert File.string_contains_file_content(output, 'emulate_android_help_osx_output.txt')
        else:
            assert File.string_contains_file_content(output, 'emulate_android_help_output.txt')

    def test_213_help_run(self):
        output = run(TNS_PATH + " emulate -h")
        assert File.string_contains_file_content(output, 'run_help_output.txt')
        assert "error" not in output

    def test_214_help_device(self):
        output = run(TNS_PATH + " device -h")
        assert File.string_contains_file_content(output, 'device_help_output.txt')
        assert "error" not in output

    def test_215_help_device_Log(self):
        output = run(TNS_PATH + " device log -h")
        assert File.string_contains_file_content(output, 'devicelog_help_output.txt')
        assert "error" not in output

    def test_216_help_device_list_applications(self):
        output = run(TNS_PATH + " device list-applications -h")
        assert File.string_contains_file_content(output, 'devicelist_help_output.txt')
        assert "error" not in output

    def test_217_help_device_run(self):
        output = run(TNS_PATH + " device emulate -h")
        assert File.string_contains_file_content(output, 'devicerun_help_output.txt')
        assert "error" not in output

    def test_218_help_debug(self):
        output = run(TNS_PATH + " debug -h")
        assert File.string_contains_file_content(output, 'debug_help_output.txt')
        assert "error" not in output

    def test_219_help_debug_android(self):
        output = run(TNS_PATH + " debug android -h")
        assert File.string_contains_file_content(output, 'debug_android_help_output.txt')
        assert "error" not in output

    def test_220_help_debug_ios(self):
        output = run(TNS_PATH + " debug ios -h")
        assert File.string_contains_file_content(output, 'debug_ios_help_output.txt')
        assert "error" not in output

    def test_221_help_feature_usage_tracking(self):
        output = run(TNS_PATH + " feature-usage-tracking -h")
        assert File.string_contains_file_content(output, 'feature_help_output.txt')
        assert "error" not in output

    def test_400_help_invalid_command(self):
        output = run(TNS_PATH + " invalidCommand")
        assert "Unknown command 'invalidcommand'. Use 'tns help' for help." in output

    def test_401_help_invalid_command(self):
        output = run(TNS_PATH + " 4")
        assert "Unknown command '4'. Use 'tns help' for help." in output

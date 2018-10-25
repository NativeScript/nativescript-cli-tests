"""
Test for `help` command
"""
import unittest

from core.base_class.BaseClass import BaseClass
from core.osutils.os_type import OSType
from core.settings.settings import IOS_PACKAGE, ANDROID_PACKAGE, CURRENT_OS
from core.tns.tns import Tns


class HelpTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    def setUp(self):
        BaseClass.setUp(self)

    @classmethod
    def verify_help(cls, output):
        strings = ['Synopsis', 'Usage']
        for str in strings:
            assert str in output

    def test_001_help(self):
        output = Tns.run_tns_command("--help")

        assert "NativeScript" in output
        assert "General Commands" in output
        assert "Project Development Commands" in output
        assert "Publishing Commands" in output
        assert "Device Commands" in output
        assert "Global Options" in output

    def test_102_create_app_help(self):
        output = Tns.run_tns_command("create --help")

        assert "Template" in output
        assert "Synopsis" in output
        assert "create" in output
        assert "Options" in output
        assert "Arguments" in output
        assert "Angular based" in output
        assert "predefined template" in output

    def test_103_platform_add_help(self):
        output = Tns.run_tns_command("platform add --help")

        HelpTests.verify_help(output)
        assert "platform add" in output
        assert "Arguments" in output
        assert "Options" in output
        assert "Android latest" in output

        if CURRENT_OS == OSType.OSX:
            assert "iOS latest runtime" in output
        else:
            assert "iOS latest runtime" not in output

    def test_104_platform_remove_help(self):
        output = Tns.run_tns_command("platform remove --help")

        HelpTests.verify_help(output)
        assert "platform remove" in output
        assert "android" in output

        if CURRENT_OS == OSType.OSX:
            assert "ios" in output
            assert "Arguments" in output
        else:
            assert "ios" not in output
            assert "Arguments" not in output

    def test_105_update_help(self):
        output = Tns.run_tns_command("platform update --help")

        HelpTests.verify_help(output)
        assert "platform update" in output
        assert "Android selected runtime" in output
        assert "Arguments" in output

        if CURRENT_OS == OSType.OSX:
            assert "iOS latest runtime" in output
        else:
            assert "iOS latest runtime" not in output

    def test_106_prepare_help(self):
        output = Tns.run_tns_command("prepare --help")

        HelpTests.verify_help(output)
        assert "prepare" in output
        assert "android" in output

        if CURRENT_OS == OSType.OSX:
            assert "ios" in output
            assert "Arguments" in output
        else:
            assert "ios" not in output
            assert "Arguments" not in output

    def test_107_build_help(self):
        output = Tns.run_tns_command("build --help")

        HelpTests.verify_help(output)
        assert "build" in output
        assert "android" in output

        if CURRENT_OS == OSType.OSX:
            assert "ios" in output
            assert "Arguments" in output
        else:
            assert "ios" not in output
            assert "Arguments" not in output

    def test_108_deploy_help(self):
        output = Tns.run_tns_command("deploy --help")

        assert "Description" in output
        assert "deploy" in output
        assert "device" in output
        assert "release" in output

        if CURRENT_OS == OSType.OSX:
            HelpTests.verify_help(output)
            assert "Deploy on iOS" in output
            assert "Deploy on Android" in output
        else:
            assert "Deploy on iOS" not in output
            assert "Options" in output

    def test_109_run_help(self):
        output = Tns.run_tns_command("run --help")

        HelpTests.verify_help(output)
        assert "run" in output
        assert "Options" in output
        assert "release" in output
        assert "device" in output

        if CURRENT_OS == OSType.OSX:
            assert "ios" in output
            assert "Arguments" in output
        else:
            assert "ios" not in output
            assert "Arguments" not in output

    def test_110_debug_help(self):
        output = Tns.run_tns_command("debug --help")

        HelpTests.verify_help(output)
        assert "debug" in output
        assert "android" in output

        if CURRENT_OS == OSType.OSX:
            assert "ios" in output
            assert "Arguments" in output
        else:
            assert "ios" not in output
            assert "Arguments" not in output

    def test_111_test_help(self):
        output = Tns.run_tns_command("test --help")

        HelpTests.verify_help(output)
        assert "test" in output
        assert "android" in output

        if CURRENT_OS == OSType.OSX:
            assert "ios" in output
            assert "Arguments" in output
        else:
            assert "ios" not in output
            assert "Arguments" not in output

    def test_112_install_help(self):
        output = Tns.run_tns_command("install -h")

        HelpTests.verify_help(output)
        assert "install" in output
        assert "Arguments" in output
        assert "Options" in output
        assert "path" in output

    def test_113_plugin_help(self):
        output = Tns.run_tns_command("plugin --help")

        HelpTests.verify_help(output)
        assert "plugin" in output
        assert "add" in output
        assert "remove" in output
        assert "update" in output
        assert "create" in output
        assert "Arguments" in output

    def test_114_device_log_help(self):
        output = Tns.run_tns_command("device log --help")

        HelpTests.verify_help(output)
        assert "device log" in output
        assert "Options" in output
        assert "device" in output

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_115_run_ios_help(self):
        output = Tns.run_tns_command("run ios --help")

        HelpTests.verify_help(output)
        assert "syncAllFiles" in output
        assert "env.*" in output
        assert "bundle" in output
        assert "justlaunch" in output
        assert "sdk" in output

    def test_116_run_android_help(self):
        output = Tns.run_tns_command("run android --help")

        HelpTests.verify_help(output)
        assert "syncAllFiles" in output
        assert "env.*" in output
        assert "bundle" in output
        assert "justlaunch" in output
        assert "key-store-path" in output

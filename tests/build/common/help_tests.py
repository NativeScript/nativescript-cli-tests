import os
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import BRANCH
from core.settings.strings import *
from core.tns.tns import Tns
from core.settings.settings import IOS_RUNTIME_PATH, CURRENT_OS, OSType, TEST_RUN_HOME, ANDROID_RUNTIME_PATH, \
    PROVISIONING


class HelpTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def test_101_help(self):
        output = Tns.run_tns_command("--help")

        assert "NativeScript" in output
        assert "General Commands" in output
        assert "Project Development Commands" in output
        assert "Publishing Commands" in output
        assert "Device Commands" in output
        assert "Global Options" in output

    def test_102_create_app_help(self):
        output = Tns.run_tns_command("create --help")

        assert "create" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "Options" in output
        assert "Angular template" in output
        assert "Create from default" in output

    def test_103_platform_add_help(self):
        output = Tns.run_tns_command("platform add --help")

        assert "platform add" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "Options" in output
        assert "Android latest" in output
        assert "iOS latest runtime" in output

    def test_104_platform_remove_help(self):
        output = Tns.run_tns_command("platform remove --help")

        assert "platform remove" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "Platform" in output

    def test_105_update_help(self):
        output = Tns.run_tns_command("platform update --help")

        assert "platform update" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "Android selected runtime" in output
        assert "iOS latest runtime" in output

    def test_106_prepare_help(self):
        output = Tns.run_tns_command("prepare --help")

        assert "prepare" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "android" in output
        assert "ios" in output

    def test_107_build_help(self):
        output = Tns.run_tns_command("build --help")

        assert "build" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "android" in output
        assert "ios" in output

    def test_108_deploy_help(self):
        output = Tns.run_tns_command("deploy --help")

        assert "deploy" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Options for iOS" in output
        assert "Options for Android" in output
        assert "Attributes" in output
        assert "device" in output
        assert "release" in output

    def test_109_run_help(self):
        output = Tns.run_tns_command("run --help")

        assert "run" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Options" in output
        assert "Attributes" in output
        assert "release" in output
        assert "device" in output

    def test_110_debug_help(self):
        output = Tns.run_tns_command("debug --help")

        assert "debug" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "android" in output
        assert "ios" in output

    def test_111_test_help(self):
        output = Tns.run_tns_command("test --help")

        assert "test" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "android" in output
        assert "ios" in output

    def test_112_install_help(self):
        output = Tns.run_tns_command("install -h")

        assert "install" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Arguments" in output
        assert "Options" in output
        assert "path" in output

    def test_113_plugin_help(self):
        output = Tns.run_tns_command("plugin --help")

        assert "plugin" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "add" in output
        assert "remove" in output
        assert "update" in output
        assert "find" in output
        assert "search" in output

    def test_114_device_log_help(self):
        output = Tns.run_tns_command("device log --help")

        assert "device log" in output
        assert "Synopsis" in output
        assert "Usage" in output
        assert "Attributes" in output
        assert "Options" in output
        assert "device" in output
"""
Test that check CLI package after installation.
"""
import unittest

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS


class SetupTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @unittest.skipIf(CURRENT_OS != OSType.OSX, 'Skip on Linux and Windows')
    def test_001_mac_script_has_execution_permissions(self):
        output = run('ls -la node_modules/nativescript/setup/mac-startup-shell-script.sh')
        assert "-rwxr-xr-x" in output, "macOS script has not execution permissions."

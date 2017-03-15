"""
Test for `tns --version` command
"""
import re

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *


class VersionTests(BaseClass):
    def test_001_version(self):
        output = Tns.run_tns_command("", attributes={"--version": ""})
        version = re.compile("^\\d+\\.\\d+\\.\\d+(-\\S+)?$").match(output)
        assert version, invalid_version.format(output)

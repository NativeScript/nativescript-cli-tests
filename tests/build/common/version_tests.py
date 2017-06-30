"""
Test for `tns --version` command
"""
import re

from core.base_class.BaseClass import BaseClass
from core.tns.tns import Tns


class VersionTests(BaseClass):
    def test_001_version(self):
        version = Tns.version()
        match = re.compile("^\\d+\\.\\d+\\.\\d+(-\\S+)?$").match(version)
        assert match, "{0} is not a valid version.".format(version)

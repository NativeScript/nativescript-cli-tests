"""
Test for usage-reporting command
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.settings.settings import TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns


class UsageReportingTests(BaseClass):
    config = os.path.join(TEST_RUN_HOME, 'node_modules', 'nativescript', 'config', 'config.json')

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_usage_reporting_enable(self):
        output = Tns.run_tns_command("usage-reporting enable")
        assert enabled.format(usage_reporting, "now ") in output
        assert "GA_TRACKING_ID" in File.read(self.config)
        assert "UA-111455-44" in File.read(self.config)

        # Check there is message for tracking in Google Analytics
        output = Tns.run_tns_command("doctor", timeout=180, log_trace=True)
        assert "Will send the following information to Google Analytics" in output

        output = Tns.run_tns_command("usage-reporting status")
        assert enabled.format(usage_reporting, "") in output

        # https://github.com/NativeScript/nativescript-cli/issues/3595
        output = Tns.create_app(self.app_name,
                                attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                                log_trace=True,
                                force_clean=False, update_modules=True)
        assert "label: 'data/apps/livesync-hello-world.tgz'" not in output
        assert "label: 'localTemplate_tns-template-hello-world'" in output

    def test_002_usage_reporting_disable(self):
        output = Tns.run_tns_command("usage-reporting disable")
        assert disabled.format(usage_reporting, "now ") in output
        assert "GA_TRACKING_ID" in File.read(self.config)
        assert "UA-111455-44" in File.read(self.config)

        # Check there is no any message for tracking in Google Analytics
        output = Tns.run_tns_command("doctor", timeout=180, log_trace=True)
        assert "Will send the following information to Google Analytics" not in output

        output = Tns.run_tns_command("usage-reporting status")
        assert disabled.format(usage_reporting, "") in output

    def test_401_usage_reporting_with_invalid_parameter(self):
        output = Tns.run_tns_command("usage-reporting " + invalid)
        assert invalid_value.format(invalid) in output

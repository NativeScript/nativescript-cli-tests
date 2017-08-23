"""
Test for --provision options
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, DEVELOPMENT_TEAM, \
    PROVISIONING, DISTRIBUTION_PROVISIONING
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSProvisioningTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Xcode.cleanup_cache()
        Tns.create_app(cls.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Simulator.stop()

    def tearDown(self):
        BaseClass.tearDown(self)
        assert not Simulator.is_running()[0], "Simulator started after " + self._testMethodName

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup(cls.app_name)

    def test_200_build_ios_list_provisions(self):
        output = Tns.build_ios(attributes={"--path": self.app_name, "--provision": ""}, assert_success=False)
        assert "Provision Name" in output
        assert "Provision UUID" in output
        assert "App Id" in output
        assert "Team" in output
        assert "Type" in output
        assert "Due" in output
        assert "Devices" in output
        assert PROVISIONING in output
        assert DISTRIBUTION_PROVISIONING in output
        assert DEVELOPMENT_TEAM in output

    def test_201_build_ios_with_provision(self):
        build_attributes = {"--path": self.app_name, "--forDevice": "", "--release": "", "--provision": PROVISIONING}
        Tns.build_ios(attributes=build_attributes)

    def test_202_build_ios_with_distribution_provision(self):
        build_attributes = {"--path": self.app_name, "--forDevice": "", "--release": "",
                            "--provision": DISTRIBUTION_PROVISIONING}
        Tns.build_ios(attributes=build_attributes)

    def test_400_build_ios_with_wrong_provision(self):
        output = Tns.build_ios(attributes={"--path": self.app_name, "--provision": "fake"}, assert_success=False)
        assert "Failed to find mobile provision with UUID or Name: fake" in output

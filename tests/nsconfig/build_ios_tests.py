"""
Test for building projects for iOS platform with different nsconfig setup.
"""
from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import PROVISIONING, \
    DISTRIBUTION_PROVISIONING, DEVELOPMENT_TEAM, TEST_RUN_HOME
from core.tns.tns import Tns
from core.xcode.xcode import Xcode
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class BuildiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocation"):
            assert "ChangeAppLocation" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocation"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocation", TEST_RUN_HOME + "/ChangeAppLocation")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndName",
                        TEST_RUN_HOME + "/ChangeAppLocationAndName")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocation", TEST_RUN_HOME + "/ChangeAppResLocation")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRoot",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRoot")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameApp", TEST_RUN_HOME + "/RenameApp")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppRes", TEST_RUN_HOME + "/RenameAppRes")
        else:
            CreateNSConfigApps.createApps()

        if not File.exists(TEST_RUN_HOME + "/ChangeAppLocation"):
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocation", TEST_RUN_HOME + "/ChangeAppLocation")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndName",
                        TEST_RUN_HOME + "/ChangeAppLocationAndName")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocation", TEST_RUN_HOME + "/ChangeAppResLocation")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRoot",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRoot")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameApp", TEST_RUN_HOME + "/RenameApp")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppRes", TEST_RUN_HOME + "/RenameAppRes")
        else:
            assert File.exists(TEST_RUN_HOME + "/ChangeAppLocation")

        Xcode.cleanup_cache()

    def setUp(self):
        BaseClass.setUp(self)
        Simulator.stop()

    def tearDown(self):
        BaseClass.tearDown(self)
        assert not Simulator.is_running()[0], "Simulator started after " + self._testMethodName

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup("ChangeAppLocation")
        Folder.cleanup("ChangeAppLocationAndName")
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("ChangeAppResLocationInRoot")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")
        Folder.cleanup("ChangeAppLocation.app")
        File.remove("ChangeAppLocation.ipa")
        File.remove("ChangeAppLocation-ipa.tgz")
        Folder.cleanup("ChangeAppLocationAndName.app")
        File.remove("ChangeAppLocationAndName-ipa.tgz")
        File.remove("ChangeAppLocationAndName.ipa")
        Folder.cleanup("ChangeAppResLocation.app")
        File.remove("ChangeAppResLocation-ipa.tgz")
        File.remove("ChangeAppResLocation.ipa")
        Folder.cleanup("ChangeAppResLocationInRoot.app")
        File.remove("ChangeAppResLocationInRoot-ipa.tgz")
        File.remove("ChangeAppResLocationInRoot.ipa")
        Folder.cleanup("RenameApp.app")
        File.remove("RenameApp.ipa")
        File.remove("RenameApp-ipa.tgz")
        Folder.cleanup("RenameAppRes.app")
        File.remove("RenameAppRes.ipa")
        File.remove("RenameAppRes-ipa.tgz")

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_001_build_ios(self, app_name):
        Tns.build_ios(attributes={"--path": app_name}, log_trace=True)
        Tns.build_ios(attributes={"--path": app_name, "--forDevice": "", "--release": ""}, log_trace=True)

        # Verify no aar and frameworks in platforms folder
        assert not File.pattern_exists(app_name + "/platforms/ios", "*.aar")
        assert not File.pattern_exists(app_name + "/platforms/ios/" + app_name + "/app/tns_modules", "*.framework")

        # Verify ipa has both armv7 and arm64 archs
        run("mv " + app_name + "/platforms/ios/build/device/" + app_name + ".ipa " + app_name + "-ipa.tgz")
        run("unzip -o " + app_name + "-ipa.tgz")
        output = run("lipo -info Payload/" + app_name + ".app/" + app_name)
        Folder.cleanup("Payload")
        assert "Architectures in the fat file: Payload/" + app_name + ".app/" + app_name + " are: armv7 arm64" in output

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_190_build_ios_distribution_provisions(self, app_name):
        # Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": app_name}, assert_success=False)

        # List all provisions and verify them
        output = Tns.build_ios(attributes={"--path": app_name, "--provision": ""}, assert_success=False)
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

        # Build with correct distribution provision
        build_attributes = {"--path": app_name, "--forDevice": "", "--release": "",
                            "--provision": DISTRIBUTION_PROVISIONING}
        Tns.build_ios(attributes=build_attributes)

        # Verify that passing wrong provision shows user friendly error
        output = Tns.build_ios(attributes={"--path": app_name, "--provision": "fake"}, assert_success=False)
        assert "Failed to find mobile provision with UUID or Name: fake" in output

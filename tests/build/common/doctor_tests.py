"""
Tests for doctor command
"""
import os

from core.base_class.BaseClass import BaseClass
from core.npm.npm import Npm
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS
from core.tns.tns import Tns


class DoctorTests(BaseClass):
    ANDROID_HOME = os.environ.get("ANDROID_HOME")
    JAVA_HOME = os.environ.get("JAVA_HOME")

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        os.environ["ANDROID_HOME"] = self.ANDROID_HOME
        os.environ["JAVA_HOME"] = self.JAVA_HOME

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_doctor(self):
        output = Tns.run_tns_command("doctor", timeout=180)
        assert "No issues were detected." in output
        assert "Your ANDROID_HOME environment variable is set and points to correct directory." in output
        assert "Your adb from the Android SDK is correctly installed." in output
        assert "The Android SDK is installed." in output
        assert "A compatible Android SDK for compilation is found." in output
        assert "Javac is installed and is configured properly." in output
        assert "The Java Development Kit (JDK) is installed and is configured properly." in output
        if CURRENT_OS != OSType.OSX:
            assert "Local builds for iOS can be executed only on a macOS system." in output
        else:
            assert "Xcode is installed and is configured properly." in output
            assert "xcodeproj is installed and is configured properly." in output
            assert "CocoaPods are installed." in output
            assert "CocoaPods update is not required." in output
            assert "CocoaPods are configured properly." in output
            assert "Your current CocoaPods version is newer than 1.0.0" in output
            assert "Python installed and configured correctly." in output
            assert "The Python 'six' package is found." in output

    def test_200_doctor_show_warning_when_new_components_are_available(self):
        Tns.create_app(self.app_name, update_modules=False)

        Tns.platform_add_android(version="2.2.0", attributes={"--path": self.app_name})
        Npm.uninstall(package="tns-core-modules", folder=self.app_name)
        Npm.install(package="tns-core-modules@3", folder=self.app_name)
        out_doctor = Tns.run_tns_command("doctor", attributes={"--path": self.app_name}, timeout=180)
        out_info = Tns.run_tns_command("info", attributes={"--path": self.app_name}, timeout=180)
        for output in (out_doctor, out_info):
            assert "Update available for component tns-core-modules" in output
            assert "Update available for component tns-android" in output
            assert "Component tns-ios is not installed." in output

    def test_400_doctor_should_detect_wrong_path_to_android_sdk(self):
        os.environ["ANDROID_HOME"] = "WRONG_PATH"
        output = Tns.run_tns_command("doctor", timeout=180)
        assert "There seem to be issues with your configuration." in output
        assert "The ANDROID_HOME environment variable is not set or it points to a non-existent directory" in output

    def test_401_doctor_should_detect_wrong_path_to_java(self):
        os.environ["JAVA_HOME"] = "WRONG_PATH"
        output = Tns.run_tns_command("doctor", timeout=180)
        assert "Error executing command 'javac'." in output
        assert "The Java Development Kit (JDK) is not installed or is not configured properly." in output

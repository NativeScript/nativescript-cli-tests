"""
Test for specific needs of Android runtime.
"""
import os
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, EMULATOR_ID
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from core.tns.tns_platform_type import Platform

class RuntimeTests(BaseClass):
    custom_js_file = os.path.join(BaseClass.app_name, "app", "my-custom-class.js")
    tns_folder = os.path.join(BaseClass.app_name, TnsAsserts.PLATFORM_ANDROID_SRC_MAIN_PATH, "java", "com", "tns")
    gen_folder = os.path.join(tns_folder, "gen")
    generated_java_file = os.path.join(tns_folder, "MyJavaClass.java")

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.ensure_available()
        Folder.cleanup('./' + cls.app_name)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_200_calling_custom_generated_classes_declared_in_manifest(self):
        Tns.create_app(self.app_name, attributes={"--template": os.path.join("data", "apps", "sbg-test-app.tgz")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_PACKAGE, "--path": self.app_name})
        Adb.clear_logcat(device_id=EMULATOR_ID)
        Tns.run_android(attributes={"--path": self.app_name, "--device": EMULATOR_ID, "--justlaunch": ""})
        sleep(10)
        output = Adb.get_logcat(device_id=EMULATOR_ID)

        # make sure app hasn't crashed
        assert "Displayed org.nativescript.TNSApp/com.tns.ErrorReportActivity" not in output, \
            "App crashed with error activity"
        # check if we got called from custom activity that overrides the default one
        assert "we got called from onCreate of custom-nativescript-activity.js" in output, "Expected output not found"
        # make sure we called custom activity declared in manifest
        assert "we got called from onCreate of my-custom-class.js" in output, "Expected output not found"

    def test_300_verbose_log_android(self):
        Tns.create_app(self.app_name,
                       attributes={"--template": os.path.join("data", "apps", "verbose-hello-world.tgz")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_PACKAGE, "--path": self.app_name})

        output = File.read(os.path.join(self.app_name, "app", "app.js"), print_content=True)
        assert "__enableVerboseLogging()" in output, "Verbose logging not enabled in app.js"

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        sleep(10)

        log_string = File.read(log)
        assert "TNS.Native" in log_string, "__enableVerboseLogging() do not enable TNS.Native logs!"
        assert "TNS.Java" in log_string, "__enableVerboseLogging() do not enable TNS.Java logs!"

    def test_301_native_package_starting_with_in_are_working(self):
        """
         Test that native packages starting with in could be accessed
        """

        # Change main-page.js so it contains only logging information
        source_js = os.path.join('data', "issues", 'android-runtime-1046', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)
        # Change app app.gradle so it contains the dependencies to com.github.myinnos:AwesomeImagePicker:1.0.2
        source_js = os.path.join('data', "issues", 'android-runtime-1046', 'app.gradle')
        target_js = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'app.gradle')
        File.copy(src=source_js, dest=target_js)
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)

        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application'
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=240, check_interval=10, clean_log=False)
        try:
            Tns.wait_for_log(log_file=log, string_list=["###TEST PASSED###"], timeout=60, check_interval=10,
                             clean_log=False)
        except Exception as e:
            print str(e)
            assert 1 == 2, 'Native packages starting with in could not be accessed'
            
    def test_302_check_if_class_implements_java_interface(self):
        """
         Test if java class implements java interface
         https://github.com/NativeScript/android-runtime/issues/739
        """
        # Change main-page.js so it contains only logging information
        source_js = os.path.join('data', "issues", 'android-runtime-739', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)

        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=240, check_interval=10, clean_log=False)
        try:
            Tns.wait_for_log(log_file=log, string_list=["### TEST PASSED ###"], timeout=60, check_interval=10,
                             clean_log=False)
        except Exception as e:
            print str(e)
            assert 1 == 2, 'Check(instanceof) for java class implements java interface does not work' \
                           '(myRunnable instanceof java.lang.Runnable)'

    def test_303_support_HeapByteBuffer_to_ArrayBuffer(self):
        """
         Test support HeapByteBuffer to ArrayBuffer
         https://github.com/NativeScript/android-runtime/issues/1060
        """
        # Change main-page.js so it contains only logging information
        source_js = os.path.join('data', "issues", 'android-runtime-1060', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=['Successfully synced application'], timeout=240, check_interval=10, clean_log=False)
        try:
            Tns.wait_for_log(log_file=log, string_list=["###TEST PASSED###"], timeout=60, check_interval=10,
                             clean_log=False)
        except Exception as e:
            print str(e)
            assert 1 == 2, 'HeapByteBuffer to ArrayBuffer conversion is not working'
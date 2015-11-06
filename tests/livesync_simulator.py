import subprocess
import time
import unittest

import psutil

from helpers._os_lib import cleanup_folder, replace, cat_app_file
from helpers._tns_lib import ANDROID_RUNTIME_PATH, IOS_RUNTIME_PATH, \
    create_project_add_platform, LiveSync, Run
from helpers.device import given_real_device, get_physical_device_id


# pylint: disable=R0201, C0111
class LiveSync_Simulator(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')
        given_real_device(platform="ios")
        given_real_device(platform="android")

    def tearDown(self):
        pass

    def test_001_LiveSync_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)
        run(platform="ios", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        live_sync(platform="ios", path="TNS_App")

        output = cat_app_file("ios", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

    def test_002_LiveSync_iOS_Device(self):
        device_id = get_physical_device_id(platform="ios")
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)
        run(platform="ios", path="TNS_App")

        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        live_sync(platform="ios", device=device_id, path="TNS_App")

        output = cat_app_file("ios", "TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output

    @unittest.skip("TODO: Fix.")
    def test_003_LiveSync_iOS_Watch(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)
        run(platform="ios", path="TNS_App")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")

        pr = subprocess.Popen(
            "tns livesync ios --watch --path TNS_App",
            shell=True)
        pr_pid = pr.pid

        time.sleep(60)
        print "assert"
        output = cat_app_file("ios", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")

        time.sleep(15)
        print "assert"
        output = cat_app_file("ios", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")

        time.sleep(15)
        print "assert"
        output = cat_app_file("ios", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output

        print "killing child ..."
        pr.terminate()

        time.sleep(5)
        if psutil.pid_exists(pr_pid):
            print "force killing child ..."
            pr.kill()

    @unittest.skip("Fix LiveSync for Android device.")
    def test_101_LiveSync_Android(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        live_sync(platform="android", path="TNS_App")

        output = cat_app_file("android", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

    @unittest.skip("Fix LiveSync for Android device.")
    def test_102_LiveSync_Android_Device(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        run(platform="android", path="TNS_App")

        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        live_sync(platform="android", device="030b206908e6c3c5", path="TNS_App")

        output = cat_app_file("android", "TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output

    @unittest.skip("Fix LiveSync for Android device.")
    def test_103_LiveSync_Android_Watch(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        run(platform="android", path="TNS_App")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")

        print "tns livesync android --watch --path TNS_App"
        pr = subprocess.Popen(
            "tns livesync android --watch --path TNS_App",
            shell=True)
        pr_pid = pr.pid

        time.sleep(60)
        print "assert"
        output = cat_app_file("android", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")

        time.sleep(15)
        print "assert"
        output = cat_app_file("android", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output

        time.sleep(5)
        replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")

        time.sleep(15)
        print "assert"
        output = cat_app_file("android", "TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output

        print "killing child ..."
        pr.terminate()

        time.sleep(5)
        if psutil.pid_exists(pr_pid):
            print "force killing child ..."
            pr.kill()

    def test_301_LiveSync_MultiplePlatforms(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)
        output = live_sync(path="TNS_App", assert_success=False)
        assert "Multiple device platforms detected (iOS and Android). Specify platform or device on command line" in output

'''
Tests for livesync command in context of Android emulator
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0103, C0111, R0201

import psutil, subprocess, shutil, time, unittest
from multiprocessing import Process

from helpers._os_lib import cat_app_file_on_emulator, \
    cleanup_folder, replace, remove
from helpers._tns_lib import ANDROID_RUNTIME_PATH, create_project_add_platform, \
    create_project, platform_add, run, livesync
from helpers.device import given_running_emulator, stop_emulators
from helpers.simulator import stop_simulators


class LiveSyncEmulator(unittest.TestCase):

    # TODO: Add a test for #942.

    SECONDS_TO_WAIT = 20

    @classmethod
    def setUpClass(cls):

        # setup simulator
        stop_emulators()
        stop_simulators()

        # TODO: Allow parameter for emulator name - Api23.
        given_running_emulator()
        cleanup_folder('./TNS_App')

        # setup app
        create_project(proj_name="TNS_App", copy_from="data/apps/livesync-hello-world")
        platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, \
            path="TNS_App", symlink=True)
        run(platform="android", device="emulator-5554", path="TNS_App")

        # replace
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");", "(\"globals\"); // test")

        # livesync
        command = "tns livesync android " + \
            "--emulator --device emulator-5554 --watch --path TNS_App --log trace"
        print command
        cls.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print "~~~ Killing subprocess ..."
        cls.process.terminate()

        time.sleep(2)
        if psutil.pid_exists(cls.process.pid):
            print "~~~ Forced killing subprocess ..."
            cls.process.kill()

        stop_emulators()
        cleanup_folder('TNS_App')

    def wait_for_text_in_output(self, text):
        def read_loop():
            print "~~~ Waiting for: " + text
            while True:
                line = self.process.stdout.readline()
                if text in line:
                    print " + Text \"{0}\" found in: ".format(text) + line.rstrip(),
                    break
                else:
                    print (" - " + line),

        self.run_with_timeout(self.SECONDS_TO_WAIT, read_loop)

    def run_with_timeout(self, timeout, func):
        if not timeout:
            func()
            return

        p = Process(target=func)
        p.start()

        start_time = time.time()
        end_time = start_time + timeout
        while p.is_alive():
            if time.time() > end_time:
                p.terminate()
                raise Exception("Timeout while waiting for livesync.")
            time.sleep(0.5)

    def test_001_full_livesync_android_emulator_xml_js_css_tns_files(self):
        self.wait_for_text_in_output("Page loaded 1 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_emulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = cat_app_file_on_emulator("TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = cat_app_file_on_emulator("TNSApp", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = cat_app_file_on_emulator("TNSApp", \
            "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output


    def test_101_livesync_android_emulator_watch_add_xml_file(self):
        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test/test.xml")
        self.wait_for_text_in_output("Page loaded 2 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

    def test_102_livesync_android_emulator_watch_add_js_file(self):
        shutil.copyfile("TNS_App/app/app.js", "TNS_App/app/test/test.js")
        self.wait_for_text_in_output("Page loaded 1 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.js")
        assert "application.start();" in output

    def test_103_livesync_android_emulator_watch_add_css_file(self):
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test/test.css")
        self.wait_for_text_in_output("Page loaded 2 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.css")
        assert "color: #284848;" in output

    def test_111_livesync_android_emulator_watch_change_xml_file(self):
        replace("TNS_App/app/test/test.xml", "TEST", "WATCH")
        self.wait_for_text_in_output("Page loaded 3 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.xml")
        assert "<Button text=\"WATCH\" tap=\"{{ tapAction }}\" />" in output

    def test_112_livesync_android_emulator_watch_change_js_file(self):
        replace("TNS_App/app/test/test.js", "start();", "start(); // test")
        self.wait_for_text_in_output("Page loaded 1 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.js")
        assert "application.start(); // test" in output

    def test_113_livesync_android_emulator_watch_change_css_file(self):
        replace("TNS_App/app/test/test.css", "#284848", "lightgreen")
        self.wait_for_text_in_output("Page loaded 2 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.css")
        assert "color: lightgreen;" in output

    def test_121_livesync_android_emulator_watch_delete_xml_file(self):
        remove("TNS_App/app/test/test.xml")
        self.wait_for_text_in_output("Page loaded 3 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.xml")
        assert output is None

    def test_122_livesync_android_emulator_watch_delete_js_file(self):
        remove("TNS_App/app/test/test.js")
        self.wait_for_text_in_output("Page loaded 1 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.js")
        assert output is None

    def test_123_livesync_android_emulator_watch_delete_css_file(self):
        remove("TNS_App/app/test/test.css")
        self.wait_for_text_in_output("Page loaded 2 times.")

        output = cat_app_file_on_emulator("TNSApp", "app/test/test.css")
        assert output is None

    def test_301_livesync_android_emulator_before_run(self):
        print "~~~ Killing subprocess ..."
        self.process.terminate()

        time.sleep(2)
        if psutil.pid_exists(self.process.pid):
            print "~~~ Forced killing subprocess ..."
            self.process.kill()

        cleanup_folder('TNS_App')
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        livesync(platform="android", device="emulator-5554", path="TNS_App")

        output = cat_app_file_on_emulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

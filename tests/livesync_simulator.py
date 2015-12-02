'''
Tests for livesync command in context of iOS simulator
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0103, C0111, R0201

import psutil, subprocess, shutil, time, unittest
from multiprocessing import Process

from helpers._os_lib import cleanup_folder, replace, remove
from helpers._tns_lib import IOS_RUNTIME_SYMLINK_PATH, \
    create_project, platform_add, build, run, livesync, TNS_PATH
from helpers.device import stop_emulators
from helpers.simulator import create_simulator, delete_simulator, \
    cat_app_file_on_simulator, start_simulator, stop_simulators, \
    SIMULATOR_NAME


class LiveSyncSimulator(unittest.TestCase):

    SECONDS_TO_WAIT = 120

    @classmethod
    def setUpClass(cls):

        # setup simulator
        stop_emulators()
        stop_simulators()

        delete_simulator(SIMULATOR_NAME)
        create_simulator(SIMULATOR_NAME, 'iPhone 6s', '9.0')

        start_simulator(SIMULATOR_NAME)
        cleanup_folder('TNS_App')
        cleanup_folder('appTest')

        # setup app
        create_project(proj_name="TNS_App", copy_from="data/apps/livesync-hello-world")
        platform_add(platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
            path="TNS_App", symlink=True)
        run(platform="ios", emulator=True, path="TNS_App")

        # replace
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");", "(\"globals\"); // test")

        # livesync
        command = TNS_PATH + " livesync ios --emulator --watch --path TNS_App --log trace"
        print command
        cls.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # TODO: check is --watch still running? if not - start it again?

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

        stop_simulators()
        cleanup_folder('TNS_App')
        cleanup_folder('appTest')

    def wait_for_text_in_output(self, text):
        def read_loop():
            count = 0
            found = False
            print "~~~ Waiting for: " + text

            while not found:
                if count == 0:
                    line = self.process.stdout.readline()
                    if text in line:
                        print " + Text \"{0}\" found in: ".format(text) + line.rstrip(),
                        print '\n'
                        count = 1
                        continue
                    else:
                        print (" - " + line),
                if count == 1:
                    line = self.process.stdout.readline()
                    if text in line:
                        print " + Text \"{0}\" found in: ".format(text) + line.rstrip(),
                        raise Exception("The console.log() message duplicates.")
                    else:
                        found = True
                        print (" - " + line),
                        break

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

    def test_001_full_livesync_ios_simulator_xml_js_css_tns_files(self):

        # TODO: Update with console.log() when supported on simulators ...
        self.wait_for_text_in_output("prepared")
        time.sleep(2) # ... than delete these.

        output = cat_app_file_on_simulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_simulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = cat_app_file_on_simulator("TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = cat_app_file_on_simulator("TNSApp", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = cat_app_file_on_simulator("TNSApp", \
            "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output

    def test_101_livesync_ios_simulator_watch_add_xml_file(self):
        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test/test.xml")
        self.wait_for_text_in_output("app/test/test.xml")

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

    def test_102_livesync_ios_simulator_watch_add_js_file(self):
        shutil.copyfile("TNS_App/app/app.js", "TNS_App/app/test/test.js")
        self.wait_for_text_in_output("app/test/test.js")
        time.sleep(2)

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.js")
        assert "application.start();" in output

    def test_103_livesync_ios_simulator_watch_add_css_file(self):
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test/test.css")
        self.wait_for_text_in_output("app/test/test.css")

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.css")
        assert "color: #284848;" in output

    def test_111_livesync_ios_simulator_watch_change_xml_file(self):
        replace("TNS_App/app/main-page.xml", "TEST", "WATCH")
        self.wait_for_text_in_output("app/main-page.xml")

        output = cat_app_file_on_simulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"WATCH\" tap=\"{{ tapAction }}\" />" in output

    def test_112_livesync_ios_simulator_watch_change_js_file(self):
        replace("TNS_App/app/main-view-model.js", "clicks", "tricks")
        self.wait_for_text_in_output("app/main-view-model.js")
        time.sleep(2)

        output = cat_app_file_on_simulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" tricks left\");" in output

    def test_113_livesync_ios_simulator_watch_change_css_file(self):
        replace("TNS_App/app/app.css", "#284848", "lightgreen")
        self.wait_for_text_in_output("app/app.css")

        output = cat_app_file_on_simulator("TNSApp", "app/app.css")
        assert "color: lightgreen;" in output

#     https://github.com/NativeScript/nativescript-cli/issues/1210
#     def test_121_livesync_ios_simulator_watch_delete_xml_file(self):
#         remove("TNS_App/app/test/test.xml")
#         self.wait_for_text_in_output("app/test/test.xml")
#
#         output = cat_app_file_on_simulator("TNSApp", "app/test/test.xml")
#         assert "No such file or directory" in output
#
#     def test_122_livesync_ios_simulator_watch_delete_js_file(self):
#         remove("TNS_App/app/test/test.js")
#         self.wait_for_text_in_output("app/test/test.js")
#         time.sleep(2)
#
#         output = cat_app_file_on_simulator("TNSApp", "app/test/test.js")
#         assert "No such file or directory" in output
#
#     def test_123_livesync_ios_simulator_watch_delete_css_file(self):
#         remove("TNS_App/app/test/test.css")
#         self.wait_for_text_in_output("app/test/test.css")
#
#         output = cat_app_file_on_simulator("TNSApp", "app/test/test.css")
#         assert "No such file or directory" in output

    def test_301_livesync_ios_simulator_before_run(self):
        print "~~~ Killing subprocess ..."
        self.process.terminate()

        time.sleep(2)
        if psutil.pid_exists(self.process.pid):
            print "~~~ Forced killing subprocess ..."
            self.process.kill()

        cleanup_folder('TNS_App')
        create_project(proj_name="TNS_App")
        platform_add(platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
            path="TNS_App", symlink=True)

        # replace
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");", "(\"globals\"); // test")

        livesync(platform="ios", emulator=True, path="TNS_App")

        output = cat_app_file_on_simulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_simulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = cat_app_file_on_simulator("TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = cat_app_file_on_simulator("TNSApp", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = cat_app_file_on_simulator("TNSApp", \
            "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output

#     https://github.com/NativeScript/nativescript-cli/issues/1225
#     def test_301_livesync_ios_simulator_before_run(self):
#         print "~~~ Killing subprocess ..."
#         self.process.terminate()
#
#         time.sleep(2)
#         if psutil.pid_exists(self.process.pid):
#             print "~~~ Forced killing subprocess ..."
#             self.process.kill()
#
#         cleanup_folder('appTest')
#         create_project(proj_name="appTest")
#         platform_add(platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
#             path="appTest", symlink=True)
#         build(platform="ios", path="appTest")
#
#         # replace
#         replace("appTest/app/main-page.xml", "TAP", "TEST")
#         replace("appTest/app/main-view-model.js", "taps", "clicks")
#         replace("appTest/app/app.css", "30", "20")
#
#         replace("appTest/node_modules/tns-core-modules/LICENSE", "2015", "9999")
#         replace(
#             "appTest/node_modules/tns-core-modules/application/application-common.js",
#             "(\"globals\");", "(\"globals\"); // test")
#
#         livesync(platform="ios", emulator=True, path="appTest")
#         self.wait_for_text_in_output("prepared")
#         time.sleep(2)
#
#         output = cat_app_file_on_simulator("appTest", "app/main-page.xml")
#         assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
#         output = cat_app_file_on_simulator("appTest", "app/main-view-model.js")
#         assert "this.set(\"message\", this.counter + \" clicks left\");" in output
#         output = cat_app_file_on_simulator("appTest", "app/app.css")
#         assert "font-size: 20;" in output
#
#         output = cat_app_file_on_simulator("appTest", "app/tns_modules/LICENSE")
#         assert "Copyright (c) 9999 Telerik AD" in output
#         output = cat_app_file_on_simulator("appTest", \
#             "app/tns_modules/application/application-common.js")
#         assert "require(\"globals\"); // test" in output

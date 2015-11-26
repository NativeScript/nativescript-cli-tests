'''
Tests for livesync command in context of iOS simulator
'''

# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111, R0201

import psutil, subprocess, time, unittest

from helpers._os_lib import cleanup_folder, replace
from helpers._tns_lib import IOS_RUNTIME_SYMLINK_PATH, \
    create_project, platform_add, run, live_sync
from helpers.device import stop_emulators
from helpers.simulator import create_simulator, delete_simulator, \
    cat_app_file_on_simulator, start_simulator, stop_simulators


class LiveSyncSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        stop_emulators()
        stop_simulators()

        delete_simulator('iPhone 6s 90')
        create_simulator('iPhone 6s 90', \
            'iPhone 6s', '9.0')

        start_simulator('iPhone 6s 90')
        cleanup_folder('TNS_App')

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

#     @classmethod
#     def tearDownClass(cls):
#         stop_simulators()
#         cleanup_folder('TNS_App')

    def test_001_livesync_watch(self):
        def wait_for_text_in_output(text):
            while True:
                line = proc.stdout.readline()
                if text in line:
                    print "Text \"{0}\" found in: ".format(text), line.rstrip()
                    time.sleep(2)
                    break

        create_project(proj_name="TNS_App", copy_from="data/apps/livesync-hello-world")
        platform_add(platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
            path="TNS_App", symlink=True)
        run(platform="ios", emulator=True, path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");",
            "(\"globals\"); // test")

        command = "tns livesync ios --emulator --watch --path TNS_App --log trace"
        print command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc_pid = proc.pid

        # TODO: To be updated with console.log() when supported.
        wait_for_text_in_output("prepared")

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

        print "Killing child process ..."
        proc.terminate()

        time.sleep(2)
        if psutil.pid_exists(proc_pid):
            print "Force killing child process ..."
            proc.kill()

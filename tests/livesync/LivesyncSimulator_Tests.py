"""
Tests for livesync command in context of iOS simulator
"""

import shutil
import time

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.watcher import Watcher
from core.settings.settings import SIMULATOR_NAME, IOS_RUNTIME_SYMLINK_PATH, TNS_PATH, DeviceType
from core.tns.tns import Tns


#########################################
# test_001
#   -> first run the app and then run full sync with xml, css and js
#   -> verify if simualtor is started run and livesync reuse running simulators
# test_101 - test_133
#   -> test livesync --watch with xml,css,js and add/delete files
# test_301
#   -> run full sync directly with out run before that
#########################################
from tests.livesync.livesync_helper import replace_all, verify_all_replaced


class LivesyncSimulator_Tests(Watcher):
    app_name = "TNS_App"
    app_name_appTest = "appTest"

    @classmethod
    def setUpClass(cls):

        # setup simulator
        Emulator.stop_emulators()
        Simulator.stop_simulators()

        Simulator.delete(SIMULATOR_NAME)
        Simulator.create(SIMULATOR_NAME, 'iPhone 6', '9.0')
        Simulator.create(SIMULATOR_NAME, 'iPhone 6', '9.1')
        Simulator.create(SIMULATOR_NAME, 'iPhone 6', '9.2')

        Simulator.start(SIMULATOR_NAME, '9.1')
        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_appTest)

        # setup app
        Tns.create_app(cls.app_name, attributes={"--copy-from": "data/apps/livesync-hello-world"})
        Tns.platform_add_ios(attributes={"--path": cls.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.run_ios(attributes={"--emulator": "",
                                         "--path": cls.app_name,
                                         "--justlaunch": ""},
                             assert_success=False)
        assert "Starting iOS Simulator" not in output

        # replace
        replace_all(app_name=cls.app_name)

        # livesync
        command = TNS_PATH + " livesync ios --emulator --watch --path " + cls.app_name + " --log trace"
        print command
        cls.start_watcher(command)

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
        cls.terminate_watcher()
        Simulator.stop_simulators()

        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_appTest)

    def test_001_full_livesync_ios_simulator_xml_js_css_tns_files(self):
        self.wait_for_text_in_output("prepared")
        time.sleep(3)  # ... than delete these.
        verify_all_replaced(device_type=DeviceType.SIMULATOR, app_name="TNSApp")

    # Add new files
    def test_101_livesync_ios_simulator_watch_add_xml_file(self):
        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/test/test.xml")
        self.wait_for_text_in_output("app/test/test.xml to")

        Simulator.file_contains("TNSApp", "app/test/test.xml", text="TEST")

    def test_102_livesync_ios_simulator_watch_add_js_file(self):
        shutil.copyfile(self.app_name + "/app/app.js", self.app_name + "/app/test/test.js")
        self.wait_for_text_in_output("app/test/test.js to")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/test/test.js", text="application.start")

    def test_103_livesync_ios_simulator_watch_add_css_file(self):
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/test/test.css")
        self.wait_for_text_in_output("app/test/test.css to")
        time.sleep(1)
        Simulator.file_contains("TNSApp", "app/test/test.css", text="color: #284848;")

    # Change in files
    def test_111_livesync_ios_simulator_watch_change_xml_file(self):
        File.replace(self.app_name + "/app/main-page.xml", "TEST", "WATCH")
        self.wait_for_text_in_output("app/main-page.xml to")
        time.sleep(1)
        Simulator.file_contains("TNSApp", "app/main-page.xml", text="WATCH")

    def test_112_livesync_ios_simulator_watch_change_js_file(self):
        File.replace(self.app_name + "/app/main-view-model.js", "clicks", "tricks")
        self.wait_for_text_in_output("app/main-view-model.js to")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/main-view-model.js", text="tricks left")

    def test_113_livesync_ios_simulator_watch_change_css_file(self):
        File.replace(self.app_name + "/app/app.css", "#284848", "green")
        self.wait_for_text_in_output("app/app.css to")
        Simulator.file_contains("TNSApp", "app/app.css", text="color: green;")

    # Delete files
    def test_121_livesync_ios_simulator_watch_delete_xml_file(self):
        File.remove(self.app_name + "/app/test/test.xml")
        self.wait_for_text_in_output("app/test/test.xml")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/test/test.xml", text="No such file or directory")

    def test_122_livesync_ios_simulator_watch_delete_js_file(self):
        File.remove(self.app_name + "/app/test/test.js")
        self.wait_for_text_in_output("app/test/test.js")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/test/test.js", text="No such file or directory")

    def test_123_livesync_ios_simulator_watch_delete_css_file(self):
        File.remove(self.app_name + "/app/test/test.css")
        self.wait_for_text_in_output("app/test/test.css")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/test/test.css", text="No such file or directory")

    # Add files to a new folder
    def test_131_livesync_ios_simulator_watch_add_xml_file_to_new_folder(self):
        Folder.create(self.app_name + "/app/folder")
        self.wait_for_text_in_output(self.app_name + "/app/folder/")
        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/folder/test.xml")
        self.wait_for_text_in_output("app/folder/test.xml file with")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/folder/test.xml", text="WATCH")
    #         remove(self.app_name + "/app/folder")
    #         self.wait_for_text_in_output("app/folder/")
    #
    #         Simulator.file_contains("TNSApp", "app/folder/test.xml")
    #         assert "No such file or directory" in output

    def test_132_livesync_ios_simulator_watch_add_js_file_to_new_folder(self):
        shutil.copyfile(self.app_name + "/app/app.js", self.app_name + "/app/folder/test.js")
        self.wait_for_text_in_output("app/folder/test.js to")
        time.sleep(3)
        Simulator.file_contains("TNSApp", "app/folder/test.js", text="application.start")

    def test_133_livesync_ios_simulator_watch_add_css_file_to_new_folder(self):
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/folder/test.css")
        self.wait_for_text_in_output("app/folder/test.css to")
        time.sleep(1)
        Simulator.file_contains("TNSApp", "app/folder/test.css", text="color: green;")

    def test_301_livesync_ios_simulator_before_run(self):

        # TODO: Add test for https://github.com/NativeScript/nativescript-cli/issues/1548 after it is fixed

        self.terminate_watcher()
        Folder.cleanup(self.app_name_appTest)
        Simulator.stop_simulators()
        Tns.create_app(self.app_name_appTest)
        Tns.platform_add_ios(attributes={"--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--path": self.app_name_appTest,
                                         "--symlink": ""
                                         })

        # replace
        File.replace(self.app_name_appTest + "/app/main-page.xml", "TAP", "MYTAP")
        File.replace(self.app_name_appTest + "/app/main-view-model.js", "taps", "clicks")
        File.replace(self.app_name_appTest + "/app/app.css", "30", "20")

        File.replace(self.app_name_appTest + "/node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright")
        File.replace(self.app_name_appTest + "/node_modules/tns-core-modules/application/application-common.js",
                     "(\"globals\");", "(\"globals\"); // test")

        output = Tns.livesync(platform="ios", attributes={"--emulator": "",
                                                          "--path": self.app_name_appTest,
                                                          "--justlaunch": ""})
        assert "Successfully synced application org.nativescript.appTest" in output
        time.sleep(3)

        Simulator.file_contains(self.app_name_appTest, "app/main-page.xml", text="MYTAP")
        Simulator.file_contains(self.app_name_appTest, "app/main-view-model.js", text="clicks left")
        Simulator.file_contains(self.app_name_appTest, "app/app.css", text="font-size: 20;")
        Simulator.file_contains(self.app_name_appTest, "app/tns_modules/LICENSE", text="MyCopyright")
        Simulator.file_contains(self.app_name_appTest, "app/tns_modules/application/application-common.js",
                                text="require(\"globals\"); // test")

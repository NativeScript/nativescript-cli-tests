import shutil
import time

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.watcher import Watcher
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, DeviceType
from core.tns.tns import Tns
from tests.livesync.livesync_helper import verify_all_replaced, replace_all


class LivesyncEmulatorWatch_Tests(Watcher):
    app_name = "TNS_App"
    app_name_appTest = "appTest"
    # TODO: Add a test for #942.

    @classmethod
    def setUpClass(cls):
        # setup emulator
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_appTest)

        # setup app
        Tns.create_app(cls.app_name, attributes={"--copy-from": "data/apps/livesync-hello-world"})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH,
                                             "--path": cls.app_name
                                             })
        Tns.run_android(attributes={"--device": "emulator-5554",
                                    "--path": cls.app_name,
                                    "--justlaunch": ""})

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
        cls.terminate_watcher()
        Emulator.stop_emulators()

        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_appTest)

    def test_001_full_livesync_android_emulator_xml_js_css_tns_files(self):
        replace_all(app_name=self.app_name)

        command = TNS_PATH + " livesync android --emulator --device emulator-5554 --watch --path " + self.app_name
        self.start_watcher(command)
        time.sleep(10)
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        verify_all_replaced(device_type=DeviceType.EMULATOR, app_name=self.app_name)

    # Add new files
    def test_101_livesync_android_emulator_watch_add_xml_file(self):
        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/test/test.xml")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/test/test.xml", text="TEST")

    def test_102_livesync_android_emulator_watch_add_js_file(self):
        shutil.copyfile(self.app_name + "/app/app.js", self.app_name + "/app/test/test.js")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/test/test.js", text="application.start")

    def test_103_livesync_android_emulator_watch_add_css_file(self):
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/test/test.css")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/test/test.css", text="color: #284848;")

    # Change in files
    def test_111_livesync_android_emulator_watch_change_xml_file(self):
        File.replace(self.app_name + "/app/main-page.xml", "TEST", "WATCH")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/main-page.xml", text="WATCH")

    def test_112_livesync_android_emulator_watch_change_js_file(self):
        File.replace(self.app_name + "/app/main-view-model.js", "clicks", "tricks")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/main-view-model.js", text="tricks left")

    def test_113_livesync_android_emulator_watch_change_css_file(self):
        File.replace(self.app_name + "/app/app.css", "#284848", "green")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/app.css", text="color: green;")

        # Delete files

    #     def test_121_livesync_android_emulator_watch_delete_xml_file(self):
    #         remove(self.app_name + "/app/test/test.xml")
    #         self.wait_for_text_in_output("Page loaded 3 times")
    #
    #         Emulator.file_contains("TNSApp", "app/test/test.xml")
    #         assert "No such file or directory" in output
    #
    #     def test_122_livesync_android_emulator_watch_delete_js_file(self):
    #         remove(self.app_name + "/app/test/test.js")
    #         self.wait_for_text_in_output("Page loaded 1 times")
    #
    #         Emulator.file_contains("TNSApp", "app/test/test.js")
    #         assert "No such file or directory" in output
    #
    #     def test_123_livesync_android_emulator_watch_delete_css_file(self):
    #         remove(self.app_name + "/app/test/test.css")
    #         self.wait_for_text_in_output("Page loaded 2 times")
    #
    #         Emulator.file_contains("TNSApp", "app/test/test.css")
    #         assert "No such file or directory" in output

    # Add files to a new folder
    def test_131_livesync_android_emulator_watch_add_xml_file_to_new_folder(self):
        Folder.create(self.app_name + "/app/folder")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/folder/test.xml")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/folder/test.xml", text="WATCH")

    #         remove(self.app_name + "/app/folder")
    #         self.wait_for_text_in_output("app/folder/") ???
    #
    #         Emulator.file_contains("TNSApp", "app/folder/test.xml")
    #         assert "No such file or directory" in output

    def test_132_livesync_android_emulator_watch_add_js_file_to_new_folder(self):
        shutil.copyfile(self.app_name + "/app/app.js", self.app_name + "/app/folder/test.js")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/folder/test.js", text="application.start")

    def test_133_livesync_android_emulator_watch_add_css_file_to_new_folder(self):
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/folder/test.css")
        self.wait_for_text_in_output("Successfully synced application", timeout=30)
        time.sleep(10)
        Emulator.file_contains("TNSApp", "app/folder/test.css", text="color: green;")

import unittest

from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, VERBOSE_LOG, EMULATOR_NAME
from core.tns.tns import Tns


class VerboseLogEmulator(unittest.TestCase):
    app_name = "TNS_App"

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup(self.app_name)
        File.remove(VERBOSE_LOG)
        Emulator.stop_emulators()

    def tearDown(self):
        Folder.cleanup(self.app_name)
        Emulator.stop_emulators()

    def test_101_verbose_log_android(self):
        Tns.create_app(self.app_name, attributes={"--copy-from": "data/apps/verbose-hello-world"})
        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path=self.app_name)
        output = run(TNS_PATH + " run android --emulator --device " + EMULATOR_NAME +
                     " --justlaunch --path " + self.app_name, 180, output=True, file_name=VERBOSE_LOG)
        assert "Project successfully built" in output

        File.cat(self.app_name + "/app/app.js")
        lines = output.split('\n')
        count = len(lines)

        print "The verbose log contains {} lines.".format(str(count))
        assert count < 1000,\
            "The verbose log contains more than 1000 lines. It contains {} lines.".format(str(count))
        assert "***" not in output, "The verbose log contains an exception."

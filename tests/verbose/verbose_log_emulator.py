import unittest

from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, VERBOSE_LOG
from core.tns.tns import Tns


class VerboseLogEmulator(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('TNS_App')
        File.remove(VERBOSE_LOG)
        Emulator.stop_emulators()

    def tearDown(self):
        Folder.cleanup('TNS_App')
        Emulator.stop_emulators()

    def test_101_verbose_log_android(self):
        Tns.create_app(app_name="TNS_App", copy_from="data/apps/verbose-hello-world")
        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path="TNS_App")
        output = run(TNS_PATH + " run android --emulator --justlaunch --path TNS_App", 180, output=True, file_name=VERBOSE_LOG)
        assert "Project successfully built" in output

        File.cat("TNS_App/app/app.js")
        lines = output.split('\n')
        count = len(lines)

        print "The verbose log contains {} lines.".format(str(count))
        assert count < 1000,\
            "The verbose log contains more than 1000 lines. It contains {} lines.".format(str(count))
        assert "***" not in output, "The verbose log contains an exception."

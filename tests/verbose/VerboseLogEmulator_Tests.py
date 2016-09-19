import os

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, VERBOSE_LOG
from core.tns.tns import Tns


class VerboseLogEmulator(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        File.remove(VERBOSE_LOG)
        Emulator.stop_emulators()
        Emulator.ensure_available()

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)
        Emulator.stop_emulators()

    def test_101_verbose_log_android(self):
        Tns.create_app(self.app_name, attributes={"--copy-from": os.path.join("data", "apps", "verbose-hello-world")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH,
                                             "--path": self.app_name
                                             })

        output = File.cat(os.path.join(self.app_name, "app", "app.js"))
        assert "__enableVerboseLogging()" in output, "Verbose logging not enabled in app.js"

        output = Tns.run_android(attributes={"--emulator": "",
                                             "--justlaunch": "",
                                             "--path": self.app_name,
                                             },
                                 timeout=180)
        assert "Project successfully built" in output
        lines = output.split('\n')
        count = len(lines)

        print "The verbose log contains {} lines.".format(str(count))
        assert count < 1000, \
            "The verbose log contains more than 1000 lines. It contains {} lines.".format(str(count))
        assert "***" not in output, "The verbose log contains an exception."

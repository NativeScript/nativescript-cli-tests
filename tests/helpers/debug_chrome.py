from time import sleep

from enum import Enum

from core.chrome.chrome import Chrome
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.process import Process
from core.tns.tns import Tns


class DebugMode(Enum):
    DEFAULT = 0
    START = 1


class DebugChromeHelpers(object):

    @staticmethod
    def attach_chrome(log, mode=DebugMode.DEFAULT, port="41000"):
        """
        Attach chrome dev tools and verify logs:
        1. Wait until debug URL is available on commandline.
        2. Start Chrome and open debug URL
        3. Wait until log says debugger is attached.

        :type log: Log file of `tns debug ios` command.
        :type mode: Debug mode type.
        :type port: Default debug port for chrome debugging.
        """

        # Check initial logs
        strings = ["Setting up debugger proxy...", "Press Ctrl + C to terminate, or disconnect.",
                   "Opened localhost", "To start debugging, open the following URL in Chrome"]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Attach Chrome DevTools
        url = run(command="grep chrome-devtools " + log)
        text_log = File.read(log)
        assert "chrome-devtools://devtools/bundle" in text_log, "Debug url not printed in output of 'tns debug ios'."
        assert "localhost:" + port in text_log, "Wrong port of debug url:" + url
        Chrome.start(url)

        # Verify debugger attached
        strings = ["Frontend client connected", "Backend socket created"]
        if mode != DebugMode.START:
            strings.extend(["Loading inspector modules",
                            "Finished loading inspector modules",
                            "NativeScript debugger attached"])
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Verify debugger not disconnected
        sleep(10)
        output = File.read(log)
        assert "socket closed" not in output, "Debugger disconnected."
        assert "detached" not in output, "Debugger disconnected."
        assert not Process.is_running('NativeScript Inspector'), "iOS Inspector running instead of ChromeDev Tools."

    @staticmethod
    def assert_not_detached(log):
        output = File.read(log)
        assert "socket created" in output, "Debugger not attached at all.\n Log:\n" + output
        assert "socket closed" not in output, "Debugger disconnected.\n Log:\n" + output
        assert "detached" not in output, "Debugger disconnected.\n Log:\n" + output

    @staticmethod
    def verify_debugger_started(log):
        strings = ['NativeScript Debugger started', 'To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    @staticmethod
    def verify_debugger_started_first(log):
        # when you start 'tns debug android' for first time, missing: 'NativeScript Debugger started',
        strings = ['To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    @staticmethod
    def verify_debugger_attach(log):
        strings = ['To start debugging', 'Chrome', 'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output
        assert "NativeScript Debugger started" not in output

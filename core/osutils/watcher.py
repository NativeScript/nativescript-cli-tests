"""
This class implements Watcher Base Class.
"""

import subprocess
import time
import unittest
from multiprocessing import Process

import psutil

from core.osutils.file import File
from core.settings.settings import OUTPUT_FILE, TEST_LOG


class Watcher(unittest.TestCase):
    @classmethod
    def start_watcher(cls, command):
        print command
        # remove output.txt
        File.remove(OUTPUT_FILE)
        # append to commads.txt
        File.append(TEST_LOG, command)
        cls.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    def wait_for_text_in_output(self, text, timeout=240):
        def read_loop():
            count = 0
            found = False
            print "~~~ Waiting for: " + text

            while not found:
                if count == 0:
                    line = self.process.stdout.readline()
                    print line
                    if text in line:
                        print " + Text \"{0}\" found in: ".format(text) + line.rstrip(),
                        print '\n'
                        break

        self.run_with_timeout(timeout, read_loop)

    def run_with_timeout(self, timeout, func):
        if not timeout:
            func()
            return

        proc = Process(target=func)
        proc.start()

        start_time = time.time()
        end_time = start_time + timeout
        while proc.is_alive():
            if time.time() > end_time:
                proc.terminate()
                raise Exception("Timeout while waiting for process.")
            time.sleep(0.5)

    @classmethod
    def terminate_watcher(cls):
        print "~~~ Killing subprocess ..."
        cls.process.terminate()

        time.sleep(2)
        if psutil.pid_exists(cls.process.pid):
            print "~~~ Forced killing subprocess ..."
            cls.process.kill()

'''
This class implements Watch Base Class.
'''

# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111, R0201

import psutil, subprocess, time, unittest
from multiprocessing import Process


class WatchBaseClass(unittest.TestCase):

    SECONDS_TO_WAIT = 150

    @classmethod
    def start_watcher(cls, command):
        cls.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

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

        proc = Process(target=func)
        proc.start()

        start_time = time.time()
        end_time = start_time + timeout
        while proc.is_alive():
            if time.time() > end_time:
                proc.terminate()
                raise Exception("Timeout while waiting for livesync.")
            time.sleep(0.5)

    @classmethod
    def terminate_watcher(cls):
        print "~~~ Killing subprocess ..."
        cls.process.terminate()

        time.sleep(2)
        if psutil.pid_exists(cls.process.pid):
            print "~~~ Forced killing subprocess ..."
            cls.process.kill()

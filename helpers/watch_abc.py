'''
This class implements Watch Abstract Base Class.
'''

# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111, R0201

from abc import ABCMeta, abstractmethod
from multiprocessing import Process
import psutil, subprocess, time


class WatchABC:
    __metaclass__ = ABCMeta

    SECONDS_TO_WAIT = 120

    @abstractmethod
    def __init__(self, command):
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def terminate(self):
        print "~~~ Killing subprocess ..."
        self.process.terminate()

        time.sleep(2)
        if psutil.pid_exists(self.process.pid):
            print "~~~ Forced killing subprocess ..."
            self.process.kill()

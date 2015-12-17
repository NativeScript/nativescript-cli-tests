'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import psutil


class Process(object):

    @classmethod
    def is_running(cls, proc_name):
        result = False
        for proc in psutil.process_iter():
            if proc_name in str(proc):
                result = True
                break
        return result

    @classmethod
    def kill(cls, proc_name):
        result = False
        for proc in psutil.process_iter():
            if proc_name in str(proc):
                proc.kill()
                print "Process {0} has been killed.".format(proc_name)
                result = True
                break
        return result

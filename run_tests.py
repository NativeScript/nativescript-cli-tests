import time, os, shutil, sys, install_tns_cli
import tns_smoke_tests
from _tns_lib import *
from _os_lib import *

smokeTestResult = ""

def ExecuteTests():
    print "####RUNNING TESTS####"
    global smokeTestResult
    smokeTestResult = str(tns_smoke_tests.RunTests())

def AnalyzeResultAndExit():
    global smokeTestResult
    if not ("errors=0" in smokeTestResult) or not ("failures=0" in smokeTestResult):
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    install_tns_cli.UninstallCLI()  # remove older cli if exists
    install_tns_cli.InstallCLI()

    ExecuteTests()
    AnalyzeResultAndExit()

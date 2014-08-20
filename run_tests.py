import time, os, shutil, smtplib, sys,install_tns_cli, platform
import tns_smoke_tests
from _tns_lib import *

smokeTestResult=""
tnsTimeStamp=""

def CreateResultDirectory():
    global tnsTimeStamp
    tnsTimeStamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    currentResultDir = os.path.join("results",tnsTimeStamp)
    if not os.path.exists("results"):
        os.mkdir("results")
    os.mkdir(currentResultDir)
    return currentResultDir

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
    install_tns_cli.UninstallCLI() # remove older cli if exists
    install_tns_cli.InstallCLI()

    currentResultDir= CreateResultDirectory()
    ExecuteTests()
    shutil.copy("Report.html", os.path.join(currentResultDir,"Report.html"))
    AnalyzeResultAndExit()
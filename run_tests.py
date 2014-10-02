from helpers._tns_lib import UninstallCLI, InstallCLI
from helpers.emulator import CreateEmulator
import tns_tests_runner

smokeTestResult = ""

def ExecuteTests():
    print "####RUNNING TESTS####"
    global smokeTestResult
    smokeTestResult = str(tns_tests_runner.RunTests())

def AnalyzeResultAndExit():
    global smokeTestResult
    if not ("errors=0" in smokeTestResult) or not ("failures=0" in smokeTestResult):
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    
    CreateEmulator()
   
    UninstallCLI()  # remove older cli if exists
    InstallCLI()

    ExecuteTests()
    AnalyzeResultAndExit()
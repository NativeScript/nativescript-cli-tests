import platform
import unittest

from helpers import HTMLTestRunner
from helpers._tns_lib import GetCLIBuildVersion
from tns_tests_common import TNSTests_Common
from tns_tests_android import TNSTests_Android
from tns_tests_osx import TNSTests_OSX


def RunTests():
    
    print "Platform : ", platform.platform()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TNSTests_Common)    
    
    if 'Darwin' in platform.platform():
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TNSTests_OSX))
    else:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TNSTests_Android))
        
    with open ("Report.html", "w") as f:
        descr = "Platform : {0};  nativescript-cli build version : {1}".format(platform.platform(), GetCLIBuildVersion())
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='TNS_CLI_tests', description=descr)
        result = runner.run(suite)
    return result

if __name__ == '__main__':
    RunTests()

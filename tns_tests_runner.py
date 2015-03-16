import os
import platform
import unittest

from helpers import HTMLTestRunner
from helpers._tns_lib import GetCLIBuildVersion
from tests.build_linux import Build_Linux
from tests.build_osx import Build_OSX
from tests.create import Create
from tests.debug_linux import Debug_Linux
from tests.debug_osx import Debug_OSX
from tests.deploy_linux import Deploy_Linux
from tests.deploy_osx import Deploy_OSX
from tests.device_linux import Device_Linux
from tests.device_osx import Device_OSX
from tests.emulate_linux import Emulate_Linux
from tests.emulate_osx import Emulate_OSX
from tests.feature_usage_tracking import FeatureUsageTracking
from tests.help import Help
from tests.logtrace import LogTrace
from tests.platform_linux import Platform_Linux
from tests.platform_osx import Platform_OSX
from tests.prepare_linux import Prepare_Linux
from tests.prepare_osx import Prepare_OSX
from tests.run_linux import Run_Linux
from tests.run_osx import Run_OSX
from tests.version import Version


def RunTests():
    
    print "Platform : ", platform.platform()        
    
    # Basic suite should be able to run on all environments where Nativescript CLI can be installed
    # Basic suite does not depend on specific test environment 
    #
    # Android Requirements:
    # - Valid pair of keyStore and password
    #
    # iOS Requirements:
    # - Valid pair of certificate and provisioning profile on your OS X system
    # 
    # Following environment variables should be set:
    # - CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)
    # - ANDROID_PATH - Path to Android runtime package under test (package file should be named tns-android.tgz)   
    # - androidKeyStorePath - Specifies the file path to the keystore file which you want to use to code sign your APK  
    # - androidKeyStorePassword - Password for the keystore file
    # - androidKeyStoreAlias
    # - androidKeyStoreAliasPassword
    # - KEYCHAIN - Keychain for signing iOS Apps
    # - KEYCHAIN_PASS - Keychain password
    
    suite = unittest.TestLoader().loadTestsFromTestCase(Version)   
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Help))    
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LogTrace)) 
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FeatureUsageTracking))
               
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Create))    
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Platform_Linux))    
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Prepare_Linux)) 
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Build_Linux))
        
    if 'Darwin' in platform.platform():
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Platform_OSX))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Prepare_OSX)) 
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Build_OSX))      
    
    # TESTRUN=FULL suppose test are executed in specific test environment
    # Following Android Emulators should be available: 
    # Api17 - Android emulator with API17  
    # Api19 - Android emulator with API19
    # At least one real Android device must be attached to Linux hosts
    # At least one real iOS device must be attached to OSX hosts
    # No attached real devices on Windows hosts    
    if ('TESTRUN' in os.environ) and ("FULL" in os.environ['TESTRUN']):    
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Deploy_Linux))
            #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Run_Linux))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Emulate_Linux))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Device_Linux))       
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Debug_Linux)) 
            if 'Darwin' in platform.platform():
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Deploy_OSX))
                #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Run_OSX))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Emulate_OSX))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Device_OSX))  
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Debug_OSX))   
    else:
        # Ignore negative tests in SMOKE TEST RUN (test with id above 400)
        for test in suite:
            if test._testMethodName.find('test_4') >= 0:
                setattr(test,test._testMethodName,lambda: test.skipTest('Skip negative tests in SMOKE TEST run.'))          
                                               
    with open ("Report.html", "w") as f:
        descr = "Platform : {0};  nativescript-cli build version : {1}".format(platform.platform(), GetCLIBuildVersion())
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='TNS_CLI_tests', description=descr)
        result = runner.run(suite)
    return result

if __name__ == '__main__':
    RunTests()

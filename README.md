#nativesript-cli-tests
The NativeScript CLI integration tests

##Software Prerequisites
Install [Python](https://www.python.org/downloads/) 2.7.*

Install dependencies
```
pip install psutil 
pip install nose-parameterized
pip install pytest-timeout
```
iOS Only: Install ideviceinstaller
```
brew install ideviceinstaller
```

##Requirements
Android Requirements:
- Valid pair of keystore and password

iOS Requirements:
- Valid pair of certificate and provisioning profile on your OS X system

##Environment setup
Following environment variables should be set:

    - ACTIVE_UI - YES if machine has active UI, NO if you are runnign without UI (with NO you can run only SMOKE and DEFAULT suites)

    - TEST_RUN - Type of test run (set FULL to run all tests, see )
 
    - CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)
    
    - ANDROID_PATH - Path to Android runtime package under test (package file should be named tns-android.tgz)   
    
    - IOS_PATH - Path to iOS runtime package (should be named tns-ios.tgz)
    
    - ANDROID_KEYSTORE_PATH - Path to the keystore file
    
    - ANDROID_KEYSTORE_PASS - Password for the keystore file
    
    - ANDROID_KEYSTORE_ALIAS
    
    - ANDROID_KEYSTORE_ALIAS_PASS
    
    - KEYCHAIN - Keychain for signing iOS Apps
    
    - KEYCHAIN_PASS - Keychain password

##Test Run Types
SMOKE
- Runs tests with High priority.
DEFAULT
- All suites without dependencies on real devices  (all priorities)
- Following AVDs should be available
   Emulator-Api19-Default - Android emulator with API19
- iOS SDK 9.1, 9.2 and 9.3 should be available
FULL
- Runs all tests
- At least one real Android device must be attached to Linux hosts
- At least one real iOS device must be attached to OSX hosts

LIVESYNC
- Runs all LiveSync tests

##Run Tests

```Shell
python run_tests.py
```

##Write Tests

###Test name convention:
001 - 199 - High priority

200 - 299 - Medium priority

300 - 399 - Low priority

400 - 499 - Negative tests

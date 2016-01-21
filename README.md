nativesript-cli-tests
=====================

The NativeScript CLI integration tests

Software Prerequisites
==
Install [Python](https://www.python.org/downloads/) 2.7.*

Install dependencies
```
pip install psutil 
pip install nose-parameterized
```
iOS Only: Install ideviceinstaller
```
brew install ideviceinstaller
```

Environment setup:
==
Following environment variables should be set:

    - TEST_RUN - Type of test run (set FULL to run all tests)
 
    - CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)
    
    - ANDROID_PATH - Path to Android runtime package under test (package file should be named tns-android.tgz)   
    
    - ANDROIDKEYSTOREPATH - Specifies the file path to the keystore file which you want to use to code sign your APK  
    
    - ANDROIDKEYSTOREPASSWORD - Password for the keystore file
    
    - ANDROIDKEYSTOREALIAS
    
    - ANDROIDKEYSTOREALIASPASSWORD
    
    - KEYCHAIN - Keychain for signing iOS Apps
    
    - KEYCHAIN_PASS - Keychain password

TEST_RUN=FULL suggests test are executed in specific test environment.
For that, following should be available: 

    - Android emulator with API17 (AVD Name = Api17)
    
    - Android emulator with API19 (AVD Name = Api19)
    
    - At least one real Android device must be attached to Linux hosts
    
    - At least one real iOS device and one real Android device must be attached to OSX hosts
    

Run Tests
===

```Shell
python run_tests.py
```
===

Android Requirements:
- Valid pair of keystore and password

iOS Requirements:
- Valid pair of certificate and provisioning profile on your OS X system

Following environment variables should be set:
- CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)

- ANDROID_PATH - Path to Android runtime package (should be named tns-android.tgz)
- ANDROID_KEYSTORE_PATH - Path to the keystore file
- ANDROID_KEYSTORE_PASS - Password for the keystore file
- ANDROID_KEYSTORE_ALIAS
- ANDROID_KEYSTORE_ALIAS_PASS

- IOS_PATH - Path to iOS runtime package (should be named tns-ios.tgz)

- ACTIVE_UI - YES or NO

- TEST_RUN - types:
SMOKE
- Runs tests with High priority.
DEFAULT
- All suites without dependencies on real devices  (all priorities)
- Following AVDs should be available
   Api19 - Android emulator with API19
FULL
- Runs all tests
- At least one real Android device must be attached to Linux hosts
- At least one real iOS device must be attached to OSX hosts

LIVESYNC
- Runs all LiveSync tests

Test name convention:
001 - 199 - High priority
200 - 299 - Medium priority
300 - 399 - Low priority
400 - 499 - Negative tests

nativesript-cli-tests
=====================

The NativeScript integration tests

Software Prerequisites
==
1. Install Python 2.7.*
2. Install psutil package.

Environment setup:
==
Following environment variables should be set:

    - TESTRUN - Type of test run (set FULL to run all tests)
 
    - CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)
    
    - ANDROID_PATH - Path to Android runtime package under test (package file should be named tns-android.tgz)   
    
    - ANDROIDKEYSTOREPATH - Specifies the file path to the keystore file which you want to use to code sign your APK  
    
    - ANDROIDKEYSTOREPASSWORD - Password for the keystore file
    
    - ANDROIDKEYSTOREALIAS
    
    - ANDROIDKEYSTOREALIASPASSWORD
    
    - KEYCHAIN - Keychain for signing iOS Apps
    
    - KEYCHAIN_PASS - Keychain password

TESTRUN=FULL suggests test are executed in specific test environment.
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

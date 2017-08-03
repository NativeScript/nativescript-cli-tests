# nativesript-cli-tests
The NativeScript CLI integration tests

## Software Prerequisites
Install [Python](https://www.python.org/downloads/) 2.7.*

Install dependencies
```
pip install psutil 
pip install nose_parameterized
pip install enum34
pip install flaky
pip install uiautomator
pip install Pillow
pip install pytesseract
brew install tesseract --all-languages
```

iOS Only: Install ideviceinstaller
```
brew install ideviceinstaller --HEAD
brew install libimobiledevice --HEAD
(for iOS11 support) brew install https://gist.github.com/Haraguroicha/0dee2ee29c7376999178c5392080c16e/raw/libimobiledevice.rb --HEAD --with-ios11
```

Perf Tests Only:
```
pip install matplotlib numpy pandas
```

## Requirements
Android Requirements:
- Valid pair of keystore and password

iOS Requirements:
- Valid pair of certificate and provisioning profile on your OS X system

Note that some of the test require connected physical Android and iOS devices.

## Environment setup
Following environment variables should be set:

    - CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)
    
    - ANDROID_PATH - Path to Android runtime package under test (package file should be named tns-android.tgz)   
    
    - IOS_PATH - Path to iOS runtime package (should be named tns-ios.tgz)
    
    - ANDROID_KEYSTORE_PATH - Path to the keystore file
    
    - ANDROID_KEYSTORE_PASS - Password for the keystore file
    
    - ANDROID_KEYSTORE_ALIAS
    
    - ANDROID_KEYSTORE_ALIAS_PASS
    
    - KEYCHAIN - Keychain for signing iOS Apps
    
    - KEYCHAIN_PASS - Keychain password

## Run Tests

Run only High priority from listed folders:
```Shell
python runNose.py tests/build tests/other tests/transpilers tests/angular/CreateNG_Tests.py tests/unittests/UnitTests_Tests.py --exclude="^test_[2-9]"
```

If you run test via PyCharm and want to see console logs, please add "--nocapture" in params.

## Write Tests

### Test name convention:
001 - 199 - High priority

200 - 299 - Medium priority

300 - 399 - Low priority

400 - 499 - Negative tests

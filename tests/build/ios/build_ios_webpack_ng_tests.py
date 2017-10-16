import os
import math

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode
from core.npm.npm import Npm

class BuildiOSWebpackNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Xcode.cleanup_cache()

        # Tns.create_app_ng(app_name=cls.app_name, update_modules=True)
        # Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    # def test_101_webpack_install(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack@next", "--save-dev", folder=self.app_name)
    #     Npm.install("install", folder=self.app_name)
    #
    #     output = File.read(self.app_name + "/package.json")
    #     assert "scripts" in output
    #     assert "ns-bundle" in output
    #     assert "start-android-bundle" in output
    #     assert "start-ios-bundle" in output
    #     assert "build-android-bundle" in output
    #     assert "build-ios-bundle" in output
    #     assert "publish-ios-bundle" in output
    #     assert "generate-android-snapshot" in output
    #
    #     webpack = os.path.join(self.app_name, 'webpack.config.js')
    #     File.exists(webpack)
    #
    # def test_102_webpack_build_bundle(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name})
    #     Npm.run("build-ios-bundle", folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size > 3158000
    #     print file_info.st_size
    #
    # def test_103_webpack_build_bundle_uglify(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name})
    #     Npm.run("build-ios-bundle", option='--uglify', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    #     assert File.exists(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size < 1230000
    #     print file_info.st_size
    #
    #
    # def test_104_webpack_build_bundle_uglify_snapshot(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name})
    #     Npm.run("build-ios-bundle", option='--uglify --snapshot', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    # def test_105_webpack_build_bundle_snapshot(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name})
    #     Npm.run("build-ios-bundle", option='--snapshot', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    # def test_105_webpack_build_bundle_release(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": "", "--team-id": "CHSQ3M3P37"})
    #     Npm.run("build-ios-bundle", option='--release --forDevice', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #     assert File.exists(self.app_name + "/platforms/ios/build/device/TestApp.ipa")
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size > 3158000
    #     print file_info.st_size
    # #
    # def test_106_webpack_build_bundle_uglify_release(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": "", "--team-id": "CHSQ3M3P37"})
    #     Npm.run("build-ios-bundle", option='--uglify --release --forDevice', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #     assert File.exists(self.app_name + "/platforms/ios/build/device/TestApp.ipa")
    #     assert File.exists(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size < 1230000
    #     print file_info.st_size
    #
    # def test_107_webpack_build_bundle_snapshot_release(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": "", "--team-id": "CHSQ3M3P37"})
    #     Npm.run("build-ios-bundle", option='--snapshot --release --forDevice', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #     assert File.exists(self.app_name + "/platforms/ios/build/device/TestApp.ipa")
    #
    # def test_108_webpack_build_bundle_uglify_snapshot_release(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": "", "--team-id": "CHSQ3M3P37"})
    #     Npm.run("build-ios-bundle", option='--uglify --snapshot --release --forDevice', folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #     assert File.exists(self.app_name + "/platforms/ios/build/device/TestApp.ipa")
    #
    # def test_109_webpack_build_all_cases(self):
    #     Tns.create_app_ng(self.app_name)
    #     Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
    #     Tns.platform_add_ios(attributes={"--path": self.app_name})
    #     Tns.build_ios(attributes={"--path": self.app_name})
    #     Npm.run("build-ios-bundle", folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size > 3158000
    #     print file_info.st_size
    #
    #     Npm.run("build-ios-bundle", option='--uglify', folder=self.app_name)
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size < 1230000
    #     print file_info.st_size
    #
    #     Npm.run("build-ios-bundle", option='--uglify --snapshot', folder=self.app_name)
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size < 1230000
    #     print file_info.st_size
    #
    #     Npm.run("build-ios-bundle", option='--uglify', folder=self.app_name)
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size < 1230000
    #     print file_info.st_size
    #
    #     Npm.run("build-ios-bundle", folder=self.app_name)
    #
    #     assert File.exists(self.app_name + "/tsconfig.aot.json")
    #     assert File.exists(self.app_name + "/tsconfig.json")
    #     assert File.exists(self.app_name + "/webpack.config.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.ios.js")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
    #     assert File.exists(self.app_name + "/app/vendor-platform.android.js")
    #     assert File.exists(self.app_name + "/app/vendor.ts")
    #     assert File.exists(self.app_name + "/app/vendor.js")
    #     assert File.exists(self.app_name + "/app/main.ts")
    #     assert File.exists(self.app_name + "/app/main.js")
    #     assert File.exists(self.app_name + "/app/main.aot.ts")
    #
    #     file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
    #     assert file_info.st_size > 3158000
    #     print file_info.st_size


    def test_110_webpack_build_install_all_cases(self):
        Tns.create_app_ng(self.app_name)
        Npm.install("nativescript-dev-webpack", "--save-dev", folder=self.app_name)
        Npm.npm("install", folder=self.app_name)
        # Tns.platform_add_ios(attributes={"--path": self.app_name})
        Npm.run("build-ios-bundle", folder=self.app_name)

        assert File.exists(self.app_name + "/tsconfig.aot.json")
        assert File.exists(self.app_name + "/tsconfig.json")
        assert File.exists(self.app_name + "/webpack.config.js")
        assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
        assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
        assert File.exists(self.app_name + "/app/vendor.ts")
        assert File.exists(self.app_name + "/app/main.ts")
        assert File.exists(self.app_name + "/app/main.aot.ts")

        file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
        assert file_info.st_size > 3158000
        print file_info.st_size

        Npm.run("build-ios-bundle", option='--uglify', folder=self.app_name)
        assert File.exists(self.app_name + "/tsconfig.aot.json")
        assert File.exists(self.app_name + "/tsconfig.json")
        assert File.exists(self.app_name + "/webpack.config.js")
        assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
        assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
        assert File.exists(self.app_name + "/app/vendor.ts")
        assert File.exists(self.app_name + "/app/main.ts")
        assert File.exists(self.app_name + "/app/main.aot.ts")

        file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
        assert file_info.st_size < 1230000
        print file_info.st_size

        Npm.run("build-ios-bundle", option='--uglify --snapshot', folder=self.app_name)
        assert File.exists(self.app_name + "/tsconfig.aot.json")
        assert File.exists(self.app_name + "/tsconfig.json")
        assert File.exists(self.app_name + "/webpack.config.js")

        file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
        assert file_info.st_size < 1230000
        print file_info.st_size

        Npm.run("build-ios-bundle", option='--uglify', folder=self.app_name)
        assert File.exists(self.app_name + "/tsconfig.aot.json")
        assert File.exists(self.app_name + "/tsconfig.json")
        assert File.exists(self.app_name + "/webpack.config.js")

        file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
        assert file_info.st_size < 1230000
        print file_info.st_size

        Npm.run("build-ios-bundle", folder=self.app_name)

        assert File.exists(self.app_name + "/tsconfig.aot.json")
        assert File.exists(self.app_name + "/tsconfig.json")
        assert File.exists(self.app_name + "/webpack.config.js")
        assert File.exists(self.app_name + "/app/vendor-platform.ios.ts")
        assert File.exists(self.app_name + "/app/vendor-platform.android.ts")
        assert File.exists(self.app_name + "/app/vendor.ts")
        assert File.exists(self.app_name + "/app/main.ts")
        assert File.exists(self.app_name + "/app/main.aot.ts")

        file_info = os.stat(self.app_name + "/platforms/ios/TestApp/app/vendor.js")
        assert file_info.st_size > 3158000
        print file_info.st_size

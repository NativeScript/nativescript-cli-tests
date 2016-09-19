"""
Test for plugin* commands in context of iOS
"""

import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, IOS_RUNTIME_SYMLINK_PATH, CURRENT_OS, OSType, IOS_RUNTIME_PATH, \
    ANDROID_RUNTIME_SYMLINK_PATH, ANDROID_RUNTIME_PATH
from core.tns.tns import Tns


class PluginsiOSTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)

        # Delete derived data
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup('./' + self.app_name)

    def test_001_plugin_add_before_platform_add_ios(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})
        assert self.app_name + "/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_plugin_add_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})
        assert self.app_name + "/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_201_plugin_add_before_platform_add_ios(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "",
                                                                       "--path": self.app_name})
        if CURRENT_OS != OSType.WINDOWS:
            assert self.app_name + "/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""})
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_202_plugin_add_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "",
                                                                       "--path": self.app_name
                                                                       })
        if CURRENT_OS != OSType.WINDOWS:
            assert self.app_name + "/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_203_plugin_add_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("plugin add tns-plugin", tns_path=os.path.join("..", TNS_PATH))
        os.chdir(current_dir)
        assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_204_build_app_with_plugin_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""})

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("plugin add tns-plugin", tns_path=os.path.join("..", TNS_PATH))
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "ERROR" not in output
        assert "malformed" not in output

    def test_300_build_app_with_plugin_outside(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        output = Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})
        assert "Successfully installed plugin tns-plugin" in output

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "ERROR" not in output
        assert "malformed" not in output

    def test_301_build_app_for_both_platforms(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_SYMLINK_PATH,
                                             "--symlink": ""
                                             })

        output = Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})
        assert "Successfully installed plugin tns-plugin" in output

        # Verify files of the plugin
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test.android.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test.ios.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test2.android.xml")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test2.ios.xml")

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "ERROR" not in output
        assert "malformed" not in output

        output = Tns.build_android(attributes={"--path ": self.app_name})
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output

        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify platform specific files
        assert File.exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.js")
        assert File.exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.android.xml")

        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.js")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test2.android.xml")

    def test_302_plugin_and_npm_modules_in_same_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

        output = Tns.plugin_add("nativescript-social-share", attributes={"--path": self.app_name})
        assert "Successfully installed plugin nativescript-social-share" in output

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run("npm install nativescript-appversion --save")
        os.chdir(current_dir)
        assert "ERR!" not in output
        assert "nativescript-appversion@" in output

        output = Tns.build_android(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        # Verify plugin and npm module files
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                           "nativescript-social-share/package.json")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                           "nativescript-social-share/social-share.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                               "nativescript-social-share/social-share.android.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                               "nativescript-social-share/social-share.ios.js")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                           "nativescript-appversion/package.json")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                           "nativescript-appversion/appversion.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                               "nativescript-appversion/appversion.android.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                                               "nativescript-appversion/appversion.ios.js")

    def test_401_plugin_add_invalid_plugin(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add("wd", attributes={"--path": self.app_name}, assert_success=False)
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file " + \
               "contains a nativescript key and try again" in output

    def test_403_plugin_add_PluginNotSupportedOnSpecificPlatform(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH,
                                             "--symlink": ""
                                             })
        output = Tns.plugin_add("tns-plugin@1.0.2", attributes={"--path": self.app_name}, assert_success=False)
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output

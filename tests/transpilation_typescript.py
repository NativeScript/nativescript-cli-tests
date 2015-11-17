'''
Tests for transpilation of typescript in context
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201

import platform, unittest

from helpers._os_lib import cleanup_folder, \
    file_exists, file_with_extension_exists, is_empty, run_aut
from helpers._tns_lib import ANDROID_RUNTIME_PATH, IOS_RUNTIME_SYMLINK_PATH, \
    TNS_PATH, build, create_project, platform_add, prepare


class TranspilationTypeScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cleanup_folder('TNS_App')

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('TNS_App')

    def test_001_transpilation_typescript(self):
        create_project(proj_name="TNS_App", copy_from="template-hello-world-ts")
        platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path="TNS_App")

        assert file_with_extension_exists(
            "TNS_App/node_modules/tns-core-modules", ".d.ts")

        output = run_aut(TNS_PATH + " install typescript --path TNS_App")
        assert "TNS_App/node_modules/nativescript-dev-typescript" in output
        assert "nativescript-hook@" in output

        assert file_exists("TNS_App/tsconfig.json")
        assert file_exists("TNS_App/node_modules/typescript/bin/tsc")
        assert not is_empty("TNS_App/node_modules/nativescript-dev-typescript")
        assert file_exists("TNS_App/hooks/before-prepare/nativescript-dev-typescript.js")
        assert file_exists("TNS_App/hooks/before-watch/nativescript-dev-typescript.js")

        output = run_aut("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        output = prepare(path="TNS_App", platform="android")
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert not "error" in output

        assert file_with_extension_exists("TNS_App/app", ".js")
        assert file_with_extension_exists("TNS_App/app", ".ts")

        assert file_with_extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".js")
        assert not file_with_extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".ts")
        assert not file_with_extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules", ".ts")
        build(platform="android", path="TNS_App")

        if 'Darwin' in platform.platform():
            platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)

            output = prepare(platform="ios", path="TNS_App")
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert not "error" in output

            assert file_with_extension_exists("TNS_App/app", ".js")
            assert file_with_extension_exists("TNS_App/app", ".ts")

            assert file_with_extension_exists(
                "TNS_App/platforms/ios/TNSApp/app", ".js")
            assert not file_with_extension_exists(
                "TNS_App/platforms/ios/TNSApp/app", ".ts")
            assert not file_with_extension_exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules", ".ts")
            build(platform="ios", path="TNS_App")

    def test_201_transpilation_after_node_modules_deleted(self):
        run_aut("rm -rf TNS_App/node_modules")
        prepare(platform="android", path="TNS_App")

        # Verify that the `prepare` command
        # installs correct dependencies.
        output = run_aut("ls TNS_App/node_modules | wc -l")
        assert "3" in output, "The 'prepare' command does not install correct dependences."

from os import path
# Folders
# Console output
# Core
ios = "ios"
android = "android"
invalid = "invalidEntry"
config_debug = "CONFIGURATION Debug"
config_release = "CONFIGURATION Release"
app_identifier = "org.nativescript.testapp"

# Files
debug_apk = "TestApp-debug.apk"
release_apk = "TestApp-release.apk"
debug_apk_path = path.join("platforms", "android", "build", "outputs", "apk", debug_apk)
release_apk_path = path.join("platforms", "android", "build", "outputs", "apk", release_apk)

# Commands
autocomplete = "autocomplete"
autocompletion = "Autocompletion"
errorreporting = "error-reporting"
error_reporting = "Error reporting"
usage_reporting = "Usage reporting"
restart_shell = "Restart your shell to {0} command auto-completion."

# Info
enabled = "{0} is {1}enabled."
disabled = "{0} is {1}disabled."
available_platforms = "Available platforms for this OS:"
updates_available = "Updates available"
no_issues = "No issues were detected."
before_prepare = "Executing before-prepare hook"
peer_typeScript = "Found peer TypeScript"
skipping_prepare = "Skipping prepare."
building = "Building project..."
build_successful = "BUILD SUCCESSFUL"
installed_platforms = "Installed platforms:  {0}"
starting_simulator = "Starting iOS Simulator"
frontend_connected = "Frontend client connected"


# Project
successfully_created = "Project successfully created"
test_file_created = "Example test file created in app/tests/"
run_tests_using = "Run your tests using the \"$ tns test <platform>\" command."
successfully_prepared = "Project successfully prepared"
successfully_built = "Project successfully built"
successfully_initialized = "Project successfully initialized."
server_started = "server started"
executed_tests = "Executed 1 of 1 SUCCESS"
starting_ut_runner = "Starting browser NativeScript Unit Test Runner"
installed_on_device = "Successfully installed on device with identifier '{0}'"
copy_template_files = "Copying template files..."
"Installing tns-android"
deployed_on_device = "Successfully deployed on device"
installed_plugin = "Successfully installed plugin {0}"
tns_plugin = "tns-plugin"
codesign = "CodeSign"
nativescript_theme_core = "nativescript-theme-core"
devDependencies = "devDependencies"
started_on_device = "Successfully started on device with identifier"

# Pods
carousel = "carousel"

# Plugins

nativescript_unit_test_runner = "nativescript-unit-test-runner"
tns_core_modules = "tns-core-modules"

# Errors
error = "error"
invalid_input = "The input is not valid sub-command for '{0}' command"
invalid_option = "The option '{0}' is not supported."
invalid_value = "The value '{0}' is not valid."
no_platform = "No platform specified"
"and neither was a --path specified."
cannot_resolve_device = "Could not find device by specified identifier"
list_devices = "To list currently connected devices and verify that the specified identifier exists, run 'tns device'"
invalid_version = "{0} is not a valid version."
no_platform_installed = "No installed platforms found. Use $ tns platform add"






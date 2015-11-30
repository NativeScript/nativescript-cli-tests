'''
Wrapper around adb commands
'''

import os, time
from helpers._os_lib import run_aut


ADB_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', 'adb')

def restart_adb():
    '''Restart Adb'''
    run_aut(ADB_PATH + " kill-server")
    run_aut(ADB_PATH + " start-server")
    run_aut(ADB_PATH + " devices")

def stop_application(app_id, device_id):
    '''Stop application'''
    output = run_aut(ADB_PATH + " -s " + device_id + " shell am force-stop " + app_id)
    time.sleep(5)
    assert app_id not in output, "Failed to stop " + app_id

def is_running(app_id, device_id):
    '''Check if app is running'''
    output = run_aut(ADB_PATH + " -s " + device_id + " shell ps | grep " + app_id)
    if "org.nativescript.TNSApp" in output:
        return True
    else:
        return False

def wait_until_app_is_running(app_id, device_id, timeout=60):
    '''Waint until app is running'''
    running = False
    end_time = time.time() + timeout
    while not is_running:
        time.sleep(5)
        running = is_running(app_id, device_id)
        if running:
            break
        if (running is False) and (time.time() > end_time):
            raise NameError(app_id + " failed to start on " + \
                            device_id + " in " + timeout + " seconds.")

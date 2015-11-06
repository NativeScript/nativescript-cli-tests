'''
Wraper around adb commands
'''
import time

from time import sleep
from helpers._os_lib import run_aut

def restart_adb():
    '''Restart Adb'''
    run_aut("adb kill-server")
    run_aut("adb start-server")
    run_aut("adb devices")

def stop_application(app_id, device_id):
    '''Stop application'''
    output = run_aut("adb -s " + device_id + " shell am force-stop " + app_id)
    sleep(5)
    assert not (app_id in output), "Failed to stop " + app_id

def is_running(app_id, device_id):
    '''Check if app is running'''
    output = run_aut("adb -s " + device_id + " shell ps | grep " + app_id)
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

import time,json
from LogsTracker import *
from CacheHandler import Load_Setting

# Get setting from setting file (json)
setting = Load_Setting()

while True:
    try:
        logsTrackerService = LogsTracker_service()
        time.sleep(setting['time_to_load'])
        if logsTrackerService.LogsThreadStatus():
            print("thread didn't stop yet !!")
    except Exception as e:
        print(e)

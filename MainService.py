import time,json
import threading
from LogsTracker import *

# Get setting from setting file (json)
with open('setting/setting.json') as config_file:
    setting = json.load(config_file)


while True:
    LogsTracker(setting) #TODO: put in thread with timeout
    time.sleep(setting['time_to_load'])

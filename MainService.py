import time,json
from LogsTracker import *

# Get setting from setting file (json)
with open('setting/setting.json') as config_file:
    setting = json.load(config_file)

while True:
    LogsTracker(setting)
    time.sleep(setting['time_to_load'])


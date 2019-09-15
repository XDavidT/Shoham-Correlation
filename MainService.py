import time,json
from pymongo import MongoClient
from LogsTracker import *

with open('setting/base-setting.json') as base_setting_file:
    b_setting = json.load(base_setting_file)

# Get setting from setting file (json)
with open('setting/setting.json') as config_file:
    setting = json.load(config_file)

client = MongoClient('mongodb://'+b_setting['mongo-server']+':'+b_setting['mongo-port']+'/')
logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']] # Select DB

while True:
    LogsTracker(logs_collection,setting)
    time.sleep(setting['time_to_load'])


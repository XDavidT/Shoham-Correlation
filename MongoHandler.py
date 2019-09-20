from pymongo import MongoClient
import json

def Mongo_Connection():
    with open('setting/base-setting.json') as base_setting_file:
        b_setting = json.load(base_setting_file)

    client = MongoClient('mongodb://' + b_setting['mongo-server'] + ':' + b_setting['mongo-port'] + '/')
    return client




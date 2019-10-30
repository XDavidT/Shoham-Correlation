from pymongo import MongoClient
import json

def Mongo_Connection():
    with open('setting/base-setting.json') as base_setting_file:
        b_setting = json.load(base_setting_file)

    client = MongoClient(b_setting['mongo-server'])
    return client




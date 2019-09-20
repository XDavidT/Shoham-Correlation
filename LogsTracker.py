import datetime
from MongoHandler import Mongo_Connection
from CacheHandler import *

def LogsTracker(setting):
    events = Load_Events(setting)
    rules = Load_Rules(setting)

    client = Mongo_Connection()
    logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
    last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=setting['logs-from-X-hours'])

    for log in logs_collection.find(
            {'insert_time': {'$gte': last_time_delta}}):  # List is already from old time to last
        print(log)





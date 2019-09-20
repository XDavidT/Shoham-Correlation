import datetime
import threading as th
from MongoHandler import Mongo_Connection
from CacheHandler import *

class LogsTracker_service():
    def __init__(self):
        self.status = True
        self.thread = th.Thread(target=self.LogsTracker)
        self.thread.start()
        self.thread.join()
        self.status = False

    def LogsTracker(self):
        setting = Load_Setting()
        events = Load_Events(setting)
        rules = Load_Rules(setting)

        client = Mongo_Connection()
        logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
        last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=setting['logs-from-X-hours'])


        for event in events:                            # Search for each event
            rule = rules[event['rules'][0]['rule_id']]

            results = logs_collection.find(             # Build the query
                    {'insert_time': {'$gte': last_time_delta}},
                    {rule['field']:rule['value']})

            for log in results:  # List is already from old time to last
                print(log) # TODO: check the results

        print("thread " + str(th.get_ident()) + " finish")

    def LogsThreadStatus(self):
        return self.status







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

        logs = logs_collection.find({'insert_time': {'$gte': last_time_delta}}) # Logs from X last time

        for event in events:                            # Search for each event
            rule = rules[event['rules'][0]['rule_id']]
            print("Looking for:      " +rule['field']+ ' :  '+ str(rule['value']) )

            results = logs_collection.find(             # Build the query
                {'insert_time': {'$gte': last_time_delta},
                 rule['field']: rule['value']})

            for log in results:  # List is already from old time to last
                self.DumpDocumentToMongo(event, log)

        client.close()
        print("thread " + str(th.get_ident()) + " finish") # Dev print

    def LogsThreadStatus(self):
        return self.status

    def DumpDocumentToMongo(self,event,log):
        if(len(event['rules']) > 1):
            setting = Load_Setting()
            client = Mongo_Connection()
            log_dump = {
                'event':event['_id'],
                'step':1,
                'log':[log]
            }

            try:
                semi_open = client[setting['policy-db-name']]['semi-open']
                semi_open.insert_one(log_dump)
                print('Insert Log Status: OK.') # Dev print
            except Exception as e:
                print("Insert Log Status: Error ->"+str(e)) # Dev print

            client.close()
        elif(len(event['rules']) < 1):
            print("error - no rules in event"+ str(event['_id']))

        else:
            pass
            # TODO: make final event





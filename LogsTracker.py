import datetime


def LogsTracker(logs_collection,setting):
    last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=setting['logs-from-X-hours'])
    for log in logs_collection.find(
            {'insert_time': {'$gte': last_time_delta}}):  # List is already from old time to last
        print(log)


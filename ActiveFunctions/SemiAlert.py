import datetime
from MongoHandler import *
from CacheHandler import load_rules, load_setting, load_base_setting
from ActiveFunctions.EventDone import *


def CheckSemi():
    print("Semi-Alert Flag")

    # declaration & tools
    client = Mongo_Connection()
    b_setting = load_base_setting()
    rules = load_rules()
    semi_collection = client[b_setting['policy-db-name']][b_setting['semi-alert-collection-name']]

    semi_alert_list_size = semi_collection.find({}).count()  # Somebody waiting for me ?
    if( semi_alert_list_size == 0 ): # Nothing waiting
        print("No semi-waiting for me, until next round")  # Dev printing
        return
    # If semi-db is empty, stop the function (using 'return') - else do that:

    print("Found semi-waiting for me ! Start working !")  # Dev printing
    for log_document in semi_collection.find({}):   # find all the waiting logs
        while True:
            # Handle one document in time
            curr_step = log_document['step']
            timeout = log_document['rules'][curr_step]['timeout']
            rule_id = log_document['rules'][curr_step]['rule_id']
            rule = rules[str(rule_id)]
            last_log_time = log_document['logs'][-1]['insert_time']  # -1 take the last in array
            time_delta = last_log_time + datetime.timedelta(seconds=timeout)
            logs_collection = client[b_setting['logs-db-name']][b_setting['logs-collection-name']]

            log = FindLog(logs_collection,log_document,rule,time_delta,last_log_time)
            if (log is None):  # If nothing returned
                print("NoneType !") # Dev print
                CheckRelevant(client,log_document,time_delta,b_setting)
                break # stop while true
            else:
                # Event that complete in success will return true, then we need to break "while true"
                if HandleTheLog(semi_collection, log_document, curr_step, log):
                    SuccessEvent(client, log_document,b_setting)
                    break


    print("Flag 2# is done !")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def FindLog(logs_collection,log_document, rule,time_delta,last_log_time):
    setting = load_setting()
    if log_document['type'] == 'local':
        return logs_collection.find_one({
            rule['field']: rule['value'],  # Next rule
            setting['local_based_on']: log_document['device'],  # Same device
            'insert_time': {
                '$gte': last_log_time,  # After last log we have
                '$lte': time_delta}    # Before: (Last log + Timeout) = delta
        })     #TODO: check error massage

    elif log_document['type'] == "global":
        log_list = []
        results = logs_collection.find({
            rule['field']: rule['value'],  # Next rule
            'insert_time': {
                '$gte': last_log_time,  # After last log we have
                '$lte': time_delta}    # Before: (Last log + Timeout) = delta
        })  # After last log we have
        for log in results:
            log_list.append(log)
        return log_list
    else:
        print("Error: no log type")  # Dev print

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def HandleTheLog(semi_collection, log_document,curr_step,logs): #TODO: handle !
    if(IsDone(log_document)):
        '''
        If we update the event here to next repeat/step, and Handle was calling again,
        it mean we found the last log needed, and we can move it to Final collection.
        '''
        return True          # In this case, the function will be stop

    if log_document['rules'][curr_step]['repeated'] > log_document['curr_repeat']:
        log_document['curr_repeat'] += 1

    elif log_document['rules'][curr_step]['repeated'] == log_document['curr_repeat']:
        log_document['curr_repeat'] = 0
        log_document['step'] += 1

    else:
        print("Unknown handler ")

    if(log_document['type'] == 'local'):
        log_document['logs'].append(logs)
    else: # We have to add them one by one
        for log in logs:
            log_document['logs'].append(log)

    semi_collection.save(log_document)
    return False

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
def CheckRelevant(client,log_document,time_delta,b_setting):
    # If our time is bigger then time delta - to alert isn't relevant
    if datetime.datetime.now() > time_delta:
        FailEvent(client,log_document,b_setting)

def IsDone(log_document):
    curr_step = log_document['step']  # +1 Since step is index of rule | 0 must be count
    sum_steps = len(log_document['rules'])
    if(curr_step == (sum_steps - 1)):
        curr_repeart = log_document['curr_repeat']
        sum_repeat = log_document['rules'][curr_step]['repeated']
        if(curr_repeart == sum_repeat):
            return True
        else:
            return False
    else:
        return False

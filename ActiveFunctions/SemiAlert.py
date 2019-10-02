from ActiveFunctions.Headers import *

def CheckSemi():
    print("Semi-Alert Flag")

    # declaration & tools
    client = Mongo_Connection()
    setting = Load_Setting()
    rules = Load_Rules(setting)
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]

    semi_alert_list_size = semi_collection.find({}).count()  # Somebody waiting for me ?
    if( semi_alert_list_size == 0 ): # Nothing waiting
        print("No semi-waiting for me, until next round")
        return
    # If semi-db is empty, stop the function (using 'return') - else do that:

    print("Found semi-waiting for me ! Start working !")
    for log_document in semi_collection.find({}):   # find all the waiting logs
        # Handle one document in time
        curr_step = log_document['step']
        timeout = log_document['rules'][curr_step]['timeout']
        rule_id = log_document['rules'][curr_step]['rule_id']
        rule = rules[str(rule_id)]
        last_log_time = log_document['log'][-1]['insert_time']  # -1 take the last in array
        time_delta = last_log_time + datetime.timedelta(seconds=timeout)  # TODO: check time interval before action
        logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]

        log = FindLog(logs_collection,log_document,rule,setting,time_delta,last_log_time)
        if (len(log) == 0): # If nothing returned
            CheckRelevant(client,log_document,time_delta,setting)

        # TODO: but if something was returned - do->
    print("Flag 2# is done !")
            # step = log_document['step']+1
            # rule = rules[log_document['rules'][step]['rule_id']] # Return current rule (+1 from back one)
            # logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
            #
            # result = logs_collection.find_one({rule['field']: rule['value']})
            # # TODO: Add only if time is OK and after insert time ( of last log )
            # if (result != None): # Check if there is any result
            #
            #     semi_collection.update_one({"_id":log_document['_id']},{
            #         "$set":{            # Should change the step to current one
            #             "step": step
            #         },
            #         "$push":{           # Add to logs the new log that found
            #             "log": result
            #         }
            #     })

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

def FindLog(logs_collection,log_document, rule,setting,time_delta,last_log_time):
    if log_document['type'] == 'local':
        return logs_collection.find_one({
            rule['field']: rule['value'],  # Next rule
            setting['local_based_on']: log_document['device'],  # Same device
            "$lte": time_delta,  # Before: (Last log + Timeout) = delta
            "$get": last_log_time})  # After last log we have
    else:
        log_list = []
        results = logs_collection.find({
            rule['field']: rule['value'],  # Next rule
            "$lte": time_delta,  # Before: (Last log + Timeout) = delta
            "$get": last_log_time})  # After last log we have
        for log in results:
            log_list.append(log)
        return log_list


def ReviewLocalLog(client,log_document,log_found):
    curr_step = log_document['step']


def ReviewGlobalLog(log_document):
    pass

def CheckRelevant(client,log_document,time_delta,setting):
    # If our time is bigger then time delta - to alert isn't relevant
    if datetime.datetime.now() > time_delta:
        semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]
        fail_collection = client[setting['policy-db-name']][setting['fail-alert-collection-name']]
        fail_collection.insert_one(log_document)
        semi_collection.delete_one(log_document)


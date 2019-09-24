import asyncio
import datetime
from CacheHandler import *
from EventComplete import *
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# TODO: Separate type local/global
async def LogsTracker_service():
    print("LogsTracker_service - Flag 1#")
    # Getting all data from Cache (from db sync)
    setting = Load_Setting()
    events = Load_Events(setting)
    rules = Load_Rules(setting)

    # Get cursor to mongo collection - Client manager -> logs
    client = Mongo_Connection()
    logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
    last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=setting['logs-from-X-hours'])

    for event in events:                                          # Search for each event
        devices = []
        rule = rules[str(events[event]['rules'][0]['rule_id'])]  # Check only FIRST rule from each event
        print("Looking for:      " + rule['field'] + ' :  ' + str(rule['value']))  # Dev printing

        if events[event]['type'] is "local":
            results = logs_collection.find(  # Build the query
                {'insert_time': {'$gte': last_time_delta},  # Time delta ( X time back )
                 rule['field']: rule['value']})  # User first rule field:value
            for log in results:
                if log[setting['local_based_on']] not in devices:
                    devices.append(log[setting['local_based_on']])
                    await DumpDocumentToMongo(client,events[event],log)

        elif events[event]['type'] is "global":
            results = logs_collection.find(  # Build the query
                {'insert_time': {'$gte': last_time_delta},  # Time delta ( X time back )
                 rule['field']: rule['value']})
            for log in results:
                if log[setting['local_based_on']] not in devices:
                    devices.append(log[setting['local_based_on']])
            devices_found = len(devices)
            #TODO: insert to semi-global in mongo
        else:
            print('no event type')



        results = logs_collection.find(                 # Build the query
            {'insert_time': {'$gte': last_time_delta},  # Time delta ( X time back )
             rule['field']: rule['value']})             # User first rule field:value

        for log in results:  # List is from old time to last - > create events
            asyncio.get_event_loop().run_until_complete(DumpDocumentToMongo(client,event, log))

    client.close()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

async def DumpDocumentToMongo(client, event, log):
    # This function
    if(len(event['rules']) >= 1):    # if the event have only 1 rule, won't stop here
        setting = Load_Setting()
        log_dump = {
            'event': event['_id'],
            'step': 0, # Mean rule['0'] occur
            'log': [log],
            'rules': event['rules']
        }
        try:
            semi_open = client[setting['policy-db-name']]['semi-open']
            semi_open.insert_one(log_dump)
            print('Insert Log Status: OK.') # Dev print
        except Exception as e:
            print("Insert Log Status: Error ->"+str(e)) # Dev print

    elif( len(event['rules']) < 1 ):    # if event have less then 1 rule - its bug - we have problem.
        print("error - no rules in event"+ str(event['_id']))   # data to fix the problem

    else:   # This case is happen only if there is 1 rule in event, so go to success
        SuccessEvent()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

async def CheckSemi():
    print("Flag 2#")
    client = Mongo_Connection()
    setting = Load_Setting()
    rules = Load_Rules()
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]

    semi_alert_list_size = semi_collection.find({}).count()
    if( len(semi_alert_list_size) == 0 ): # Nothing waiting
        print("No semi-waiting for me, until next round")
        return
    else:
        print("Found semi-waiting for me ! Start working !")

        for log in semi_collection.find({}): # find all the waiting logs
            step = log['step']+1
            rule = rules[log['rules'][step]['rule_id']] # Return current rule (+1 from back one)
            logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]

            result = logs_collection.find_one({rule['field']: rule['value']})
            # TODO: Add only if time is OK and after insert time ( of last log )
            if (result != None): # Check if there is any result

                semi_collection.update_one({"_id":log['_id']},{
                    "$set":{            # Should change the step to current one
                        "step": step
                    },
                    "$push":{           # Add to logs the new log that found
                        "log": result
                    }
                })

# logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
# semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]

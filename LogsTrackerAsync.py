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
    last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=setting['logs-from-X-hours']) # Time Delta

    for event in events:                                          # Search for each event
        devices = []
        rule = rules[str(events[event]['rules'][0]['rule_id'])]  # Check only FIRST rule from each event
        print("Looking for:      " + rule['field'] + ' :  ' + str(rule['value']))  # Dev printing

        results = logs_collection.find(  # Build the query
            {'insert_time': {'$gte': last_time_delta},  # Time delta ( X time back )
             rule['field']: rule['value']})             # User first rule field:value

        # -- Local -- #
        if events[event]['type'] is "local":                # Log is LOCAL only, and need to watch it.
            for log in results:
                if log[setting['local_based_on']] not in devices:   # Based on Host/MAC/IP by prefer
                    devices.append(log[setting['local_based_on']])  # Using list check that no double log will be
                    asyncio.get_event_loop().run_until_complete(DumpDocumentToMongo(client, events[event], log,device_name=log[setting['local_based_on']]))

        # -- Global -- #
        elif events[event]['type'] is "global":             # Log is GLOBAL, and need to get the scale
            logs = []
            for log in results:                             # We only care how much Devices have the log
                if log[setting['local_based_on']] not in devices:   # No double event from same device
                    devices.append(log[setting['local_based_on']])
                    logs.append(log)
            asyncio.get_event_loop().run_until_complete(DumpDocumentToMongo(client, events[event], logs, devices=devices))

        # -- Unknown -- #
        else:
            print('no event type')

    client.close()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# Only occur once when first rule detect in event - Not Async - run_until_complete
async def DumpDocumentToMongo(client, event, log, device_name = None,devices = None):
    '''
    This statement checking that current Event have more then 1 rule in list,
    Or the rule is repeated. If so, it will create semi-event.
    Else, Jump to success and dump Final function
    '''

    if(len(event['rules']) >= 1 or event['rules'][0]['repeated'] > 1):
        setting = Load_Setting()

        log_dump = {
            'event': event['_id'],
            'step': 0,   # Mean rule['0'] occur,
            'sum_steps': len(event['rules']),
            'curr_repeat': '1',
            'type': event['type'],
            'log': [log],
            'rules': event['rules']
        }

        # If event type is global, add the devices
        if(event['type'] is "global"):
            log_dump['devices'] = devices
        # But if it's local, it's need one device per each semi-event
        else:
            log_dump['device'] = device_name

        try:
            semi_open = client[setting['policy-db-name']]['semi-open'] # TODO: add to setting semi-open-local

            '''
            We need to check that no duplicate will be in our semi-event DB
            by this statement we can assure this type of event & this device aren't there
            '''
            if ( event['type'] is "local"
                    and
                    (semi_open.find_one({'event':event['_id'], 'device':device_name}) is not None) ):
                return
            else:
                semi_open.insert_one(log_dump)
                print('Insert Log Status: OK.')           # Dev print
        except Exception as e:
            print("Insert Log Status: Error -> "+str(e))  # Dev print


    elif(len(event['rules']) is 1 and event['rules'][0]['repeated'] is 1):
        SuccessEvent()

    else:  # if event have less then 1 rule - its bug - we have problem.
        print("error - no rules in event"+ str(event['_id']))   # data to fix the problem

# When finish do nothing, the service that check Semi - will find it in db.

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

async def CheckSemi():
    print("Flag 2#")

    # declaration & tools
    client = Mongo_Connection()
    setting = Load_Setting()
    rules = Load_Rules()
    semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]

    semi_alert_list_size = semi_collection.find({}).count()
    if( semi_alert_list_size == 0 ): # Nothing waiting
        print("No semi-waiting for me, until next round")
        return
    else:
        print("Found semi-waiting for me ! Start working !")

        for log_document in semi_collection.find({}):   # find all the waiting logs

            curr_step = log_document['step']                        # Find what rule is the current rule
            rule_id = log_document['rules'][curr_step]['rule_id']
            rule = rules[rule_id]
            timeout_to_next_log = log_document['rules'][curr_step]['timeout']
            last_log_time = log_document['log'][-1]['insert_time']
            #TODO: check time interval before action

            logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]

            if log_document['type'] is 'local':
                first_log = logs_collection.find_one({rule['field']: rule['value']}) #TODO: check by device
                ReviewLocalLog(log_document)
            else:
                ReviewGlobalLog(log_document)
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

def ReviewLocalLog(log_document):
    pass
def ReviewGlobalLog(log_document):
    pass
# logs_collection = client[setting['logs-db-name']][setting['logs-collection-name']]
# semi_collection = client[setting['policy-db-name']][setting['semi-alert-collection-name']]

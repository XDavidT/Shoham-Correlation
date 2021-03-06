import datetime
from CacheHandler import load_setting, load_base_setting, load_events, load_rules
from MongoHandler import *
from termcolor import colored
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def logs_tracker_service():
    print(colored("Start Tracking",'yellow'))
    # Getting all data from Cache (from db sync)
    setting = load_setting()
    b_setting = load_base_setting()
    events = load_events()
    rules = load_rules()

    # Get cursor to mongo collection - Client manager -> logs
    client = mongo_connection()
    logs_collection = client[b_setting['logs-db-name']][b_setting['logs-collection-name']]
    last_time_delta = datetime.datetime.now() - datetime.timedelta(hours=int(setting['logs-from-X-hours']))  # TimeDelta

    for event in events:                        # Search for each event
        try:
            if events[event]['enable'] == 'false':
                continue                            # Go to next event without stopping loop
        except Exception as e:
            print("Cant check if event enable or disable\nDetails:  " + str(e))

        devices = []
        try:
            rule = rules[str(events[event]['rules'][0]['rule_id'])]  # Check only FIRST rule from each event
            print(colored("Start Checking event "+ event+" | using rule: "+rule['field'] + ' :  ' + str(rule['value']),
                          'grey','on_blue'))

            results = logs_collection.find(                 # Build the query
                {'insert_time': {'$gte': last_time_delta},  # Time delta ( X time back )
                 rule['field']: rule['value']})             # User first rule field:value

            if results.count() > 0:     # This line check that anything came up in the search
                # -- Local -- #
                if events[event]['type'] == 'Local':                # Log is LOCAL only, and need to watch it.
                    for log in results:
                        if log[setting['local_based_on']] not in devices:   # Based on Host/MAC/IP by prefer
                            devices.append(log[setting['local_based_on']])  # Using list check that no double log will be
                            DumpDocumentToMongo(client, events[event], log,device_name=log[setting['local_based_on']])

                # -- Global -- #
                elif events[event]['type'] == "Global":             # Log is GLOBAL, and need to get the scale
                    logs = []
                    for log in results:                             # We only care how much Devices have the log
                        if log[setting['local_based_on']] not in devices:   # No double event from same device
                            devices.append(log[setting['local_based_on']])
                            logs.append(log)
                    DumpDocumentToMongo(client, events[event], logs, devices=devices)

                # -- Unknown -- #
                else:
                    print('no event type - error')
            else:
                print("No logs match for that")
        except KeyError as e:
            print("Can't read event %s named: %s " % (events[event]['_id'], events[event]['name']))
            print("Details: " + e)
        except Exception as err:
            print("Unknown error, details:\n" + str(err))
    client.close()
    print(colored("Tracking Done",'grey','on_green'))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# Only occur once when first rule detect in event - Not Async - run_until_complete
def DumpDocumentToMongo(client, event, log, device_name = None,devices = None):
    print(colored("Dump to Mongo new Semi alert",'blue'))
    b_setting = load_base_setting()

    log_dump = {
        'event': event['_id'],
        'step': 0,  # Mean rule['0'] occur,
        'curr_repeat': 0,
        'type': event['type'],
        'rules': event['rules'],
        'alerts': event['alerts']
    }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Log Dump Customization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#S
    # One rule & one repeat, we done
    if (len(event['rules']) == 1 and int(event['rules'][0]['repeated']) == 1):
        log_dump['curr_repeat'] = 1

    # If the current rule need to be repeat
    elif(int(event['rules'][0]['repeated']) > 1):
        log_dump['curr_repeat'] = 1

    # Or we need to go next rule
    elif(len(event['rules']) > 1):
        log_dump['step'] = 1


    # Check for global/ local
    if(event['type'] == "Global"):
        log_dump['device'] = devices
        log_dump['logs'] = log
    # But if it's local, it's need one device per each semi-event
    else:
        log_dump['device'] = [device_name]
        log_dump['logs'] = [log]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Log Dump Customization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#E

    try:
        semi_open = client[b_setting['policy-db-name']][b_setting["semi-alert-collection-name"]]
        '''
        We need to check that no duplicate will be in our semi-event DB
        by this statement we can assure this type of event & this device aren't there
        '''
        if ( event['type'] == "Local"
                and
                (semi_open.find_one({'event':event['_id'], 'device':device_name}) is not None) ):
            print("Already in handle...")
            return
        else:
            semi_open.insert_one(log_dump)
            print(colored('Insert Log Status: OK.','blue'))           # Dev print
    except Exception as e:
        print("Insert Log Status: Error -> "+str(e))  # Dev print


# When finish do nothing, the service that check Semi - will find it in db.

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
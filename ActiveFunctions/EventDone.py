from ActionsHandlers.EmailHandler import AlertOnEmail
import datetime
from termcolor import colored

def SuccessEvent(client, log_document,b_setting):

    print(colored("Start success process",'green'))
    semi_collection = client[b_setting['policy-db-name']][b_setting["semi-alert-collection-name"]]
    success_collection = client[b_setting['policy-db-name']][b_setting['success-alert-collection-name']]
    log_document['offense_close_time'] = datetime.datetime.now()  # Discover time
    log_document.pop('step')
    log_document.pop('curr_repeat')
    log_document.pop('rules')

    # Add to new collection, but only if it done, make the delete
    try:
        success_collection.insert_one(log_document)
        try:
            semi_collection.delete_one({'_id':log_document['_id']})
            if (log_document['alerts']['email'] == 'true'):
                try:
                    AlertOnEmail(log_document)
                except Exception as e:
                    print("Error sending email, details: \n" + str(e))
                    return
        except Exception as e:
            print("Error to remove from semi-collection")
            print(e)
            return
    except Exception as e:
        print("Error to add to success DB the new offense")
        print(e)
        return



def FailEvent(client,log_document,b_setting):
    print(colored("Start success process",'red'))
    semi_collection = client[b_setting['policy-db-name']][b_setting['semi-alert-collection-name']]
    fail_collection = client[b_setting['policy-db-name']][b_setting['fail-alert-collection-name']]
    log_document['offense-close-time'] = datetime.datetime.now()
    try:
        fail_collection.insert_one(log_document)
        try:
            semi_collection.delete_one(log_document)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
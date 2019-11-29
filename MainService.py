#Functions import
from CacheHandler import main_sync,load_setting
from ActiveFunctions.LogsTracker import logs_tracker_service
from ActiveFunctions.SemiAlert import check_semi
import time


if __name__ == "__main__":
    setting = load_setting()
    while True:
        main_sync()
        counter = 1
        try:
            while counter < 4:
                logs_tracker_service()
                check_semi()
                print("Now going to sleep for %s seconds"%setting['time_to_load'])
                counter += 1
                time.sleep(int(setting['time_to_load']))
        except Exception as e:
            print(e)
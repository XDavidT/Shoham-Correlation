import asyncio

#Functions import
from CacheHandler import main_sync,load_setting
from ActiveFunctions.LogsTracker import logs_tracker_service
from ActiveFunctions.SemiAlert import check_semi


main_sync()
logs_tracker_service()
check_semi()

# async def main():
#     setting = load_setting()
#     while True:
#         LogsTracker_FirstTrigger = loop.create_task(logs_tracker_service())
#         LogsTracker_SemiAlert = loop.create_task(check_semi())
#
#         await asyncio.wait([LogsTracker_FirstTrigger, LogsTracker_SemiAlert])
#         await asyncio.sleep(setting['time_to_load'])
#
#
#
# # Get setting from setting file (json)
#
# main_sync()  # Only when starting
#
# if __name__ == "__main__":
#         try:
#             loop = asyncio.get_event_loop() # Create 'loop' to use asyncio
#             loop.run_until_complete(main())
#         except Exception as e:
#             print(e)
#         finally:
#             loop.close()
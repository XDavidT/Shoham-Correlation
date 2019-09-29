import time
# from LogsTracker import *
from LogsTrackerAsync import *
from CacheHandler import Load_Setting

LogsTracker_service()
CheckSemi()

# async def main():
#     while True:
#         LogsTracker_FirstTrigger = loop.create_task(LogsTracker_service())
#         LogsTracker_SemiAlert = loop.create_task(CheckSemi())
#
#         await asyncio.wait([LogsTracker_FirstTrigger, LogsTracker_SemiAlert])
#         await asyncio.sleep(setting['time_to_load'])
#
#
#
# # Get setting from setting file (json)
# setting = Load_Setting()
#
# if __name__ == "__main__":
#         try:
#             loop = asyncio.get_event_loop() # Create 'loop' to use asyncio
#             loop.run_until_complete(main())
#         except Exception as e:
#             print(e)
#         finally:
#             loop.close()
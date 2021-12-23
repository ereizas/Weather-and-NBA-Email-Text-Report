import threading
import time
import schedule

class emailScheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        #check if _stop_running is a valid var
        self._stop_running = threading.Event()
    
    def scheduleDaily(self,hour,minute,job):
        schedule.clear()
        schedule.every().day.at(str(hour)+":"+str(minute))
        
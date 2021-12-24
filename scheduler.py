import threading
import time
import schedule

class emailScheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        #check if _stop_running is a valid var
        self.__stop_running = threading.Event()
    
    def scheduleDaily(self,job):
        schedule.clear()
        schedule.every().day.at('8:00')
    
    #starts the program
    def run(self):
        self.__stop_running.clear()
        while not self.__stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    #ends the program
    def stop(self):
        self.__stop_running.set()

if __name__ == '__main__':
    """import email1
    em = email1.email1()
    scheduler = emailScheduler()
    scheduler.start()
    scheduler.scheduleDaily(hour,minute,em.sendEmail())
    time.sleep(30)
    scheduler.stop()"""
    pass
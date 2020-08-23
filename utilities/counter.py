import time
import threading

count = 0

def start():
    # Variables to keep track and display
    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    # Start Timer
    timeLoop = True
    while timeLoop:
        global count
        count = str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds"
        time.sleep(1)
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 24:
            hours = 0
            days += 1

counter_thread = threading.Thread(target= start)

counter_thread.start()
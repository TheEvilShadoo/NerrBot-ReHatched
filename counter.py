import time

# Variables to keep track of and display
count = 0
seconds = 0
minutes = 0
hours = 0
days = 0

def counter():
    # Start Timer
    while True:
        global count, seconds, minutes, hours, days
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

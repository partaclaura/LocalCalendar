import datetime
import time
from tkinter import messagebox, Tk


def sort_by_alarm_time(event_list):
    return sorted(event_list, key=lambda x: x.alarm_time)


def alert(title, message):
    show_method = getattr(messagebox, 'show{}'.format('info'))
    show_method(title, message)


class Session:
    def __init__(self, events):
        self.events = sort_by_alarm_time(events)
        self.start_session()

    def start_session(self):
        while self.events:
            Tk().withdraw()
            alert("test", "test")
            crt_event = self.events.pop(0)
            crt_time = datetime.datetime.now()
            print(crt_time)
            wait_time = crt_event.alarm_time - crt_time
            print(wait_time.total_seconds())
            time.sleep(wait_time.total_seconds())
            Tk().withdraw()
            alert(crt_event.metadata["name"], crt_event.metadata["description"])

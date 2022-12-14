import datetime
import threading
import time
from win10toast import ToastNotifier


def sort_by_alarm_time(event_list):
    return sorted(event_list, key=lambda x: x.alarm_time)


def handle_event(event):
    crt_time = datetime.datetime.now()
    wait_time = event.alarm_time - crt_time
    print("Alarm for {} in ".format(wait_time))
    time.sleep(wait_time.total_seconds())
    notify(event)


def build_message(event):
    return (event.metadata["description"]
            + "\n@ " + str(event.metadata["dtstart"])
            + ", " + event.metadata["location"])


def notify(event):
    n = ToastNotifier()
    message = build_message(event)
    try:
        n.show_toast(event.metadata["name"], message,
                     duration=10, icon_path="utils/Delacro-Id-Recent-Documents.ico")
    except TypeError:
        pass
    print("Event notification sent!")


class Session:
    def __init__(self, events):
        self.events = sort_by_alarm_time(events)
        self.start_session()

    def start_session(self):
        if self.events:
            while self.events:
                crt_event = self.events.pop(0)
                print("Upcoming event: {}".format(crt_event.metadata["name"]))
                t = threading.Thread(target=handle_event, args=(crt_event,))
                t.start()

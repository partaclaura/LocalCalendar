import datetime
import threading
import time
from win10toast import ToastNotifier


def sort_by_alarm_time(event_list):
    return sorted(event_list, key=lambda x: x.alarm_time)


def handle_event(event):
    crt_time = datetime.datetime.now()
    if (event.metadata["dtstart"] - crt_time).total_seconds() < event.alert_field * 60:
        print("\nMissed alarm for {}".format(event.metadata["name"]))
        notify(event, additional_info="MISSED ALARM")
    else:
        wait_time = event.alarm_time - crt_time
        print("Alarm for {} in {}".format(event.metadata["name"], str(wait_time)))
        time.sleep(wait_time.total_seconds())
        notify(event)


def build_message(event, additional_info):
    return (event.metadata["description"]
            + "\n" + additional_info
            + "\n@ " + str(event.metadata["dtstart"])
            + ", " + event.metadata["location"])


def notify(event, additional_info=""):
    n = ToastNotifier()
    message = build_message(event, additional_info)
    try:
        n.show_toast(event.metadata["name"], message,
                     duration=10, icon_path="utils/Aha-Soft-Large-Calendar-Calendar.ico")
    except TypeError:
        pass
    print("Event notification sent!")


class Session:
    def __init__(self, events):
        print("##################")
        print("Starting session...")
        self.events = sort_by_alarm_time(events)
        self.start_session()

    def start_session(self):
        if self.events:
            while self.events:
                crt_event = self.events.pop(0)
                print("\nUpcoming event: {}".format(crt_event.metadata["name"]))
                t = threading.Thread(target=handle_event, args=(crt_event,))
                t.start()
        else:
            print("\nNo upcoming events!")
        print("\nSession done! Notifications are on their way."
              + "\nRemember to take a break<3")

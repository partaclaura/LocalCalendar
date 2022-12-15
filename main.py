import os
import event
import session
from error_handling import handle_exceptions

"""
The session_calendar represents the location of the events
"""


def run_session(session_calendar, alarm_field):
    events = []
    for event_ics in os.scandir(session_calendar):
        if event_ics.is_file():
            found_event = event.LocalEvent(event_ics, alarm_field)
            if found_event.valid:
                events.append(found_event)
    session.Session(events)
    # print(s.events)


if __name__ == '__main__':
    # run_session("SampleCalendar")
    print("###### LOCAL CALENDAR ######")
    print("!Info: In this case, a calendar is represented by a folder containing events in ICS format.")
    valid = False
    path = ""
    while not valid:
        path = input("Import calendar: ")
        print("Accessing {}...".format(path))
        if not os.path.isdir(path):
            handle_exceptions(ValueError, "Not a valid calendar :( \nPlease try again...")
        else:
            found_invalid = False
            for event_file in os.scandir(path):
                if not event_file.is_file():
                    error_msg = "Some files in this dictionary don't seem to be valid events."
                    handle_exceptions(ValueError, "Not a valid calendar :( \n" + error_msg + "\nPlease try again...")
                    found_invalid = True
            if not found_invalid:
                valid = True
    valid = False
    notification_field = 1
    while not valid:
        notification_field = int(input("Receive notification: \n1. 5 minutes before"
                                       + "\n2. 10 minutes before"
                                       + "\n3. 15 minutes before"))
        if notification_field not in (1, 2, 3):
            print("Please pick a valid number choice!")
        else:
            valid = True

    match_to_field = {
        1: 5,
        2: 10,
        3: 15
    }
    run_session(path, match_to_field[notification_field])

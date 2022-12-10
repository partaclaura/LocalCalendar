import os
import event
"""
The session_calendar represents the location of the events
"""


def run_session(session_calendar):
    events = []
    for event_file in os.scandir(session_calendar):
        if event_file.is_file():
            found_event = event.LocalEvent(event_file)
            events.append(found_event)
    for e in events:
        print(e.metadata)


if __name__ == '__main__':
    run_session("SampleCalendar")


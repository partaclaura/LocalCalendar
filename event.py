from icalendar import Calendar
from datetime import timedelta


def parse_ics(ics_file):
    event_metadata = {}
    event_file = open(ics_file, 'rb')
    e = Calendar.from_ical(event_file.read())
    for component in e.walk():
        if component.name == "VEVENT":
            event_metadata["name"] = component.get("name")
            event_metadata["description"] = component.get("description")
            event_metadata["organizer"] = component.get("organizer")
            event_metadata["location"] = component.get("location")
            event_metadata["dtstart"] = component.decoded("dtstart")
            event_metadata["dtend"] = component.decoded("dtend")
    return event_metadata


def compute_alarm_time(start_date, time_before):
    alarm_time = start_date - timedelta(minutes=time_before)
    print("Event time: ", start_date)
    print("Alarm time: ", alarm_time)
    return alarm_time


class LocalEvent:

    def __init__(self, file, alarm_time):
        self.metadata = parse_ics(file)
        self.alarm_time = compute_alarm_time(self.metadata["dtstart"], alarm_time)

    def __repr__(self):
        return str((self.metadata, self.alarm_time))

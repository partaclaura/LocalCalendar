import datetime
from error_handling import handle_exceptions
from icalendar import Calendar
from datetime import timedelta
import yaml


def parse_ics(ics_file):
    event_metadata = {}
    event_file = open(ics_file, 'rb')
    e = Calendar.from_ical(event_file.read())
    for component in e.walk():
        if component.name == "VEVENT":
            # print("Component: ", component.get("name"))
            if component.get("name"):
                event_metadata["name"] = component.get("name")
            else:
                event_metadata["name"] = "Unnamed event"
            if component.get("description"):
                event_metadata["description"] = component.get("description")
            else:
                event_metadata["description"] = "No description"
            event_metadata["organizer"] = component.get("organizer")
            if component.get("location"):
                event_metadata["location"] = component.get("location")
            else:
                event_metadata["location"] = "Location Unknown"
            event_metadata["dtstart"] = component.decoded("dtstart")
            event_metadata["dtend"] = component.decoded("dtend")
    return event_metadata


def parse_yaml(yaml_file):
    event_metadata = {}
    with open(yaml_file, 'r') as file:
        ev_data = yaml.safe_load(file)
        for k in ev_data['event']:
            if k == "dtstart" or k == "dtend":
                ft = "%Y-%m-%d-%H-%M-%S"
                dt_obj = datetime.datetime.strptime(ev_data['event'][k], ft)
                event_metadata[k] = dt_obj
            else:
                event_metadata[k] = ev_data['event'][k]
    return event_metadata


def compute_alarm_time(start_date, time_before):
    alarm_time = start_date - timedelta(minutes=time_before)
    # print("Event time: ", start_date)
    # print("Alarm time: ", alarm_time)
    return alarm_time


class LocalEvent:

    def __init__(self, file, alarm_time):
        self.metadata = parse_yaml(file)
        self.alert_field = alarm_time
        self.alarm_time = compute_alarm_time(self.metadata["dtstart"], alarm_time)
        self.valid = self.validate_event()

    def __repr__(self):
        return str((self.metadata, self.alarm_time))

    def validate_event(self):
        print("##################")
        print("Validating event {}...".format(self.metadata["name"]))
        now = datetime.datetime.now()
        valid_time = now + timedelta(minutes=self.alert_field)
        if not self.metadata["dtstart"] or not self.metadata["dtend"]:
            handle_exceptions(ValueError, "Invalid event: missing info!")
            return False
        if (self.metadata["dtstart"] - datetime.datetime.now()).total_seconds() <= 0:
            handle_exceptions(ValueError, "Invalid event: already happened!")
            return False
        return True

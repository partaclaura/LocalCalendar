from icalendar import Calendar


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


class LocalEvent:

    def __init__(self, file):
        self.metadata = parse_ics(file)

def sort_by_alarm_time(event_list):
    return sorted(event_list, key=lambda x: x.alarm_time)


class Session:
    def __init__(self, events):
        self.events = sort_by_alarm_time(events)
        self.start_session()

    def start_session(self):
        while self.events:
            print(self.events.pop(0))

import datetime

class event(object):
    def __init__(self, input_end_time, input_start_time):
        self.end_time = input_end_time
        self.start_time = input_start_time

    def event_starts(hour, minute):
        if hour == self.start_time.hour and minute == self.start_time.minute:
            return True

data1 = {
  "timeMax": "2016-09-25T17:36:12.000Z",
  "kind": "calendar#freeBusy",
  "calendars": {
    "primary": {
      "busy": [
        {
          "start": "2016-09-25T00:30:00Z",
          "end": "2016-09-25T01:30:00Z"
        }
      ]
    }
  },
  "timeMin": "2016-09-24T17:36:12.000Z"
}

data2 = {
  "timeMax": "2016-09-25T17:36:12.000Z",
  "kind": "calendar#freeBusy",
  "calendars": {
    "primary": {
      "busy": [
        {
          "start": "2016-09-25T01:45:00Z",
          "end": "2016-09-25T02:00:00Z"
        }
      ]
    }
  },
  "timeMin": "2016-09-24T17:36:12.000Z"
}

event1 = event(datetime.datetime.strptime(data1['calendars']['primary']['busy'][0]['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.datetime.strptime(data1['calendars']['primary']['busy'][0]['start'], "%Y-%m-%dT%H:%M:%Sz"))
event2 = event(datetime.datetime.strptime(data2['calendars']['primary']['busy'][0]['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.datetime.strptime(data2['calendars']['primary']['busy'][0]['start'], "%Y-%m-%dT%H:%M:%Sz"))

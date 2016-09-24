import datetime

class event(object):
    def __init__(self, input_end_time, input_start_time):
        self.end_time = input_end_time
        self.start_time = input_start_time

    def event_starts(self,hour, minute):
        if hour == self.start_time.hour and minute == self.start_time.minute:
            return True
        return False
    def event_ends(self,hour, minute):
        if hour == self.end_time.hour and minute == self.end_time.minute:
            return True
        return False

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


def checkTime(event1, event2):
    event1_count = 0
    event2_count = 0
    free_zones = []
    free_zone_count = 0
    free = False
    for hour in range(24):
        for minute in range(60):
            if(event1.event_starts(hour,minute)):
                event1_count +=1
            elif (event1.event_ends(hour,minute)):
                event1_count -= 1

            if (event2.event_starts(hour,minute)):
                event2_count += 1
            elif (event2.event_ends(hour,minute)):
                event2_count -= 1

            if(event1_count==event2_count==0 and not free):
                free_zones.append([(hour,minute)])
                free = True
            elif(not event1_count==event2_count and free):
                free_zones[free_zone_count].append((hour,minute))
                free = False
                free_zone_count+=1
    if(len(free_zones)%2 != 0):
      free_zones[free_zone_count].append((23,59))
    print free_zones
    return free_zones

checkTime(event1,event2)


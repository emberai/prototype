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


class calendar(object):
    def __init__(self):
        self.my_events = []
        self.event_counter = 0

    def add_events(self, data_set):
        for time_set in data_set['calendars']['primary']['busy']:
            self.my_events.append(event(datetime.datetime.strptime(time_set['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.datetime.strptime(time_set['start'],"%Y-%m-%dT%H:%M:%Sz")))

def checkTime(cal1, cal2):
    calendar_collection = []
    calendar_collection.append(cal1)
    calendar_collection.append(cal2)
    free_zones = []
    free_zone_count = 0
    free = False

    for hour in range(24):
      for minute in range(60):
        for calendar in calendar_collection:
          for event in calendar.my_events:
            if(event.event_starts(hour,minute)):
                calendar.event_counter +=1
            elif (event.event_ends(hour,minute)):
                calendar.event_counter -= 1
          count = 0
          for calendarCHECK in calendar_collection:
            if(calendarCHECK.event_counter == 0):
              count+=1
          if(count == len(calendar_collection) and not free):
            free_zones.append([(hour,minute)])
            free = True
          elif(count != len(calendar_collection) and free):
            free_zones[free_zone_count].append((hour,minute))
            free = False
            free_zone_count+=1
    if(len(free_zones)%2 != 0):
      free_zones[free_zone_count].append((23,59))
    print free_zones
    return free_zones
##########--------------------------############

#---Sample Data---#
person1_data = {
  "timeMax": "2016-09-25T17:36:12.000Z",
  "kind": "calendar#freeBusy",
  "calendars": {
    "primary": {
      "busy": [
        {
          "start": "2016-09-25T00:00:00Z",
          "end": "2016-09-25T00:30:00Z"
        },
        {
          "start": "2016-09-25T07:00:00Z",
          "end": "2016-09-25T08:00:00Z"
        },
        {
          "start": "2016-09-25T11:00:00Z",
          "end": "2016-09-25T14:00:00Z"
        }
      ]
    }
  },
  "timeMin": "2016-09-24T17:36:12.000Z"
}

person2_data = {
  "timeMax": "2016-09-25T17:36:12.000Z",
  "kind": "calendar#freeBusy",
  "calendars": {
    "primary": {
      "busy": [
        {
          "start": "2016-09-25T00:15:00Z",
          "end": "2016-09-25T02:00:00Z"
        },
        {
          "start": "2016-09-25T10:00:00Z",
          "end": "2016-09-25T13:00:00Z"
        }
      ]
    }
  },
  "timeMin": "2016-09-24T17:36:12.000Z"
}

calendar1 = calendar()
calendar1.add_events(person1_data)
calendar2 = calendar()
calendar2.add_events(person2_data)
checkTime(calendar1,calendar2)

import datetime
import json
import os



class event(object):
    def __init__(self, input_end_time, input_start_time):
        self.end_time = input_end_time
        self.start_time = input_start_time
    #Params: hour and minute ints.
    #Returns: whether events objects start time is at that time
    def event_starts(self,hour, minute):
        if hour == self.start_time.hour and minute == self.start_time.minute:
            return True
        return False
    #Params: hour and minute ints.
    #Returns: whether events objects end time is at that time.
    def event_ends(self,hour, minute):
        if hour == self.end_time.hour and minute == self.end_time.minute:
            return True
        return False


class calendar(object):

    def __init__(self):
        self.my_events = []
        self.event_counter = 0

    #Params: parsed JSON file for individual user (contains all events)
    #adds all events as objects from provided calendar data set to the calender object
    def add_events(self, data_set):
        for time_set in data_set['calendars']['primary']['busy']:
            self.my_events.append(event(datetime.datetime.strptime(time_set['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.datetime.strptime(time_set['start'],"%Y-%m-%dT%H:%M:%Sz")))

#Params: 2 calendar objects 
#Returns: A list of size 2 lists containing start of that free block and the end of that free block.
def checkTime(cal1, cal2):
    calendar_collection = []
    calendar_collection.append(cal1)
    calendar_collection.append(cal2)
    free_zones = []
    free_zone_count = 0
    in_free_time = False

    #I apologize for this disgusting mess
    for hour in range(24):
      for minute in range(60):
        for calendar in calendar_collection:
          for event in calendar.my_events:
            if(event.event_starts(hour,minute)):
                calendar.event_counter +=1
            elif (event.event_ends(hour,minute)):
                calendar.event_counter -= 1
          #check if all cals are free
          allCalendarsFree = checkCountCalendars(calendar_collection)
          
          if(allCalendarsFree and not in_free_time):
            free_zones.append([(hour,minute)])
            in_free_time = True
          elif(not allCalendarsFree and in_free_time):
            free_zones[free_zone_count].append((hour,minute))
            in_free_time = False
            free_zone_count+=1
    #if the 2 cals are free until the end of that day
    if(len(free_zones)%2 != 0):
      free_zones[free_zone_count].append((23,59))
    print free_zones
    return free_zones
#Params: A list of calendars
#Returns: If all the calendars are free at the time checked
def checkCountCalendars(calendar_collection):
  count = 0
  for calendarCHECK in calendar_collection:
    if(calendarCHECK.event_counter == 0):
      count+=1
  return count == len(calendar_collection)
def getJSONSandcheck():
  #Curently reads 2 dummy JSON files
  

  if(os.path.isfile('calendar1.json')):
        with open('calendar1.json') as data_file:    
            calendar1_data = json.load(data_file)
  calendar1 = calendar()
  calendar1.add_events(calendar1_data)

  if(os.path.isfile('calendar2.json')):
        with open('calendar2.json') as data_file:    
            calendar2_data = json.load(data_file)
  calendar2 = calendar()
  calendar2.add_events(calendar2_data)

  checkTime(calendar1,calendar2)

getJSONSandcheck()
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

#calendar1 = calendar()
#calendar1.add_events(person1_data)
#calendar2 = calendar()
#calendar2.add_events(person2_data)
#checkTime(calendar1,calendar2)

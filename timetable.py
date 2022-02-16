import requests, json, datetime
from sys import argv
from uuid import uuid4

with open('./settings.json') as file:
    settings = json.loads(file.read())

def timeconvert(visma_time, visma_date): #function converts visma datetime format to ical datetime format
    date = datetime.datetime.strptime(visma_date, r'%d/%m/%Y') #dd/mm/yyyy
    time = datetime.datetime.strptime(visma_time, r'%H:%M').time() #hh:mm #.time() makes shure that it is a time object because combine does not accept datetime object
    fulltime = datetime.datetime.combine(date, time) #create datetime object
    icaltime = datetime.datetime.strftime(fulltime, r'%Y%m%dT%H%M00') #datetime to yyyymmddThhmmss str
    return icaltime

try:
    date = argv[1]
except IndexError:
    date = datetime.datetime.strftime(datetime.datetime.now(), r'%d/%m/%Y')

timetable = requests.get( #get timetable as json from visma
    f"https://{settings['fqdn']}/control/timetablev2/learner/{settings['vis_id']}/fetch/ALL/0/current?forWeek={date}",
    cookies = dict( Authorization = settings['Authorization'] ))
timetable = timetable.json() #convert json to python object

def ical_generator(lesson): #function to convert lesson to ical vevent
    # iCalendar specification: https://datatracker.ietf.org/doc/html/rfc5545
    global settings, timestamp
    ical_array = {
    'summary': f"SUMMARY:{lesson['teacherName']}: {lesson['subjectCode']} - {lesson['subject']}",
    'start': f"DTSTART;TZID={settings['timezone']}:{timeconvert(lesson['startTime'], lesson['date'])}",
    'end': f"DTEND;TZID={settings['timezone']}:{timeconvert(lesson['endTime'], lesson['date'])}",
    'uid': f"UID:fromvisma_{uuid4()}",
    'dtstamp': f"DTSTAMP:{timestamp}"
    }

    locations_array = lesson['locations']
    if len(locations_array) > 1:
        locations = " , ".join(locations_array)
    if len(locations_array) == 1:
        locations = locations_array[0]
    ical_array['locations'] = f"LOCATION:{locations}"

    if settings['categories'] != None:
        ical_array['categories'] = f"CATEGORIES:{settings['categories']}"

    if lesson['extraInfo'] != None:
        ical_array['description'] = f"DESCRIPTION:{lesson['extraInfo']}"

    return '\r\n'.join(['BEGIN:VEVENT', '\r\n'.join(ical_array.values()), 'END:VEVENT\r\n'])

timestamp = datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc), r'%Y%m%dT%H%M%SZ')
ical = 'BEGIN:VCALENDAR\r\nPRODID:-//Visma Inschool timetable to iCalendar/filip-nilsen.com//EN\r\nVERSION:2.0\r\n'

for lesson in timetable['timetableItems']: #iterate over lessons from the json that has been converted to a python object
    ical += ical_generator(lesson)

ical += 'END:VCALENDAR\r\n'
print(ical)

date = datetime.datetime.strftime(datetime.datetime.strptime(date, r'%d/%m/%Y'), r'%Y-%m-%d') #dd/mm/yyyy to yyyy-mm-dd
with open(f'{date}.ics', 'w') as ical_file:
    ical_file.write(ical)

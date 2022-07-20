#!/usr/bin/python3

from calendar import week
import datetime
import requests
from cal_setup import get_calendar_service
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
   
   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   #print('Getting List o 10 events')
   events_result = service.events().list(
      calendarId='primary', timeMin=now,
      maxResults=10, singleEvents=True,
      orderBy='startTime').execute()
   events = events_result.get('items', [])
   day_list = []
   events_list = []
   now_date = datetime.datetime.now(datetime.timezone.utc)
   now_day = now_date.strftime('%Y-%m-%d')
   week_more = now_date + datetime.timedelta(days=7)

   if not events:
      print('No upcoming events found.')
   for event in events:
      start = event['start'].get('dateTime', event['start'].get('date'))
      end = event['end'].get('dateTime', event['start'].get('date'))
      
      try:
         start_date = datetime.datetime.strptime(start, '%Y-%m-%d''T''%H:%M:%S%z')
         start_time = start_date.strftime('%I:%M %p')
         
      except ValueError:
         start_time = 'All day'

      try:
         end_date = datetime.datetime.strptime(end, '%Y-%m-%d''T''%H:%M:%S%z')
      except ValueError:
         end_date = ''


      if now_day in str(start_date):
         start_day = 'Today'
      elif start_date < week_more:
         start_day = start_date.strftime('%A %d')      
      else:
         start_day = start_date.strftime('%B %d')
      
      try:
         end_day = end_date.strftime('%a %d')
      except ValueError:
         end_day = ''
      except AttributeError:
         end_day = ''

      try:
         end_time = end_date.strftime('%I:%M %p')
      except ValueError:
         end_time = ''
      except AttributeError:
         end_time = ''

      try:
         location = event['location']
      except ValueError:
         location = ''
      except KeyError:
         location = ''

      event_summary = event['summary']
      day_list = (start_day, start_time, end_day, end_time, event_summary, location)
      events_list.append(day_list)
      #try:
         #print(now_day in str(start_date))
      #except Exception as e:
         #print(e)
   
   return render_template('calendar.html',
   events_list=events_list)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8011, debug=True)

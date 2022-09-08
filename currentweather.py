#!/usr/bin/python3

import requests
import datetime
import json
import config


weather_url = 'https://api.openweathermap.org/data/2.5/weather?' + config.lat_lon +'&units=imperial&appid=' + config.weather_api
weather_get = requests.get(weather_url)
weather_data = weather_get.json()

sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%I:%M %p')
sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%I:%M %p')
outside_temp = round(weather_data['main']['temp'])
real_feel = round(weather_data['main']['feels_like'])
high = round(weather_data['main']['temp_max'])
low = round(weather_data['main']['temp_min'])
humidity = weather_data['main']['humidity']
clouds = weather_data['clouds']['all']
description = weather_data['weather'][0]['description'].title()
icon = '/static/png/' + weather_data['weather'][0]['icon'] + '.png'
#icon = '/static/svg/' + weather_data['weather'][0]['icon'] + '.svg'

try:
    rain_hr = round(weather_data['rain']['1h'] / 25.4, 2)
except KeyError:
    rain_hr = 0.00
try:
    if outside_temp in range(28, 35):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 10, 2)
    elif outside_temp in range(20, 28):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 15, 2)
    elif outside_temp in range(15, 20):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 20, 2)
    elif outside_temp in range(10, 15):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 30, 2)
    elif outside_temp in range(0, 10):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 40, 2)
    elif outside_temp in range(-20, 0):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 50, 2)
    elif outside_temp in range(-100, -20):
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 100, 2)
    else:
        snow_hr = round(weather_data['snow']['1h'] / 25.4 * 1, 2)
except KeyError:
    snow_hr = 0.00

data = {'outside_temp': outside_temp,
        'real_feel': real_feel,
        'high': high,
        'low': low,
        'rain_hr': rain_hr,
        'snow_hr': snow_hr,
        'sunrise': sunrise,
        'sunset': sunset,
        'clouds': clouds,
        'description': description,
        'icon': icon,
        'humidity': humidity}

with open('/home/pi/IpadDisplay/current.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

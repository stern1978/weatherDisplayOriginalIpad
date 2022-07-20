#!/usr/bin/python3

import requests
import datetime
import json
import config


weather_url = 'https://api.openweathermap.org/data/2.5/onecall?' + config.lat_lon + '&units=imperial&appid=' + config.weather_api
weather_get = requests.get(weather_url)
weather_data = weather_get.json()
    
forecast_dict = {}
forecast_list = []
day_counter = 1
daily = weather_data['daily'][day_counter]
minute_counter = 0
minutely = weather_data['minutely']


'''for _ in minutely:
    rain_time = datetime.datetime.fromtimestamp(minutely[minute_counter]['dt']).strftime('%I:%M %p')
    rain = minutely[minute_counter]['precipitation']
    print(rain_time, rain)
    if rain != 0:
        rain_start = rain_time
    else:
        rain_start = None
    minute_counter += 1'''   

try:
    for _ in daily:
        if day_counter < 6:
            forecast_day = datetime.datetime.fromtimestamp(weather_data['daily'][day_counter]['dt']).strftime(
                '%a %d')
            forecast_max = round(weather_data['daily'][day_counter]['temp']['max'])
            forecast_min = round(weather_data['daily'][day_counter]['temp']['min'])
            forecast_icon = "/static/png/" + weather_data['daily'][day_counter]['weather'][0]['icon'] + ".png"
            forecast_description = weather_data['daily'][day_counter]['weather'][0]['description']
            forecast_pop = round(weather_data['daily'][day_counter]['pop'] * 100)
            avg_temp = (forecast_max + forecast_min) / 2
            dew_point = weather_data['current']['dew_point']
            try:
                forecast_rain = round(weather_data['daily'][day_counter]['rain'] / 25.4, 2)
            except KeyError:
                forecast_rain = 0.00
            try:
                if avg_temp in range(28, 35):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 10, 2)
                elif avg_temp in range(20, 28):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 15, 2)
                elif avg_temp in range(15, 20):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 20, 2)
                elif avg_temp in range(10, 15):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 30, 2)
                elif avg_temp in range(0, 10):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 40, 2)
                elif avg_temp in range(-20, 0):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 50, 2)
                elif avg_temp in range(-100, -20):
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 100, 2)
                else:
                    forecast_snow = round(weather_data['daily'][day_counter]['snow'] / 25.4 * 1, 2)
            except KeyError:
                forecast_snow = 0.00
            
 
            
            day_dict = {'forecast_day': forecast_day,
                        'forecast_max': forecast_max,
                        'forecast_min': forecast_min,
                        'forecast_icon': forecast_icon,
                        'forecast_pop': forecast_pop,
                        'forecast_rain': forecast_rain,
                        'forecast_snow': forecast_snow,
                        'dew_point': dew_point}

            # forecast_list.append(day_dict)
            # forecast_dict['forecast'] = forecast_list
            day_list = (forecast_day, forecast_max, forecast_min, forecast_icon, forecast_pop, forecast_rain, forecast_snow)
            forecast_list.append(day_list)
            day_counter += 1

except IndexError:
    pass


with open('/home/pi/IpadDisplay/forecast.json', 'w', encoding='utf-8') as f:
    json.dump(forecast_list, f, ensure_ascii=False, indent=4)

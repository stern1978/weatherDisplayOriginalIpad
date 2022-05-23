#!/usr/bin/python3

import requests
import json

key = 'uF0cIT4Fxu50HpPqyFqtjofmfSMdtWmVg97ZPh7c'  # os.environ.get('HUE_API')
url = "http://192.168.1.151/api/" + key + "/sensors"
room_temp = []
get = requests.get(url)
weather_data = get.json()
for num in weather_data:
    try:
        raw_temp = weather_data[num]['state']['temperature']
        temp = ((raw_temp / 100) * 9 / 5) + 32
        room_temp.append(temp)
    except KeyError:
        pass
avg_temp = {'temp': round(sum(room_temp) / len(room_temp))}

with open('/home/pi/IpadDisplay/inside.json', 'w', encoding='utf-8') as f:
    json.dump(avg_temp, f, ensure_ascii=False, indent=4)

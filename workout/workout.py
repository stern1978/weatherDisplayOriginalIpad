import requests
import pytradfri
import json
from time import sleep


tv_lignts = '51:43:A4:C1:38:7C:0B:2C'
mirror_lights = 'EB:40:A4:C1:38:9C:58:A8'
model = 'H6141'
key = {'Govee-API-Key': '821509c5-e960-486c-8553-f54cee9714d0'}
#get_url = 'https://developer-api.govee.com/v1/devices/state?device=' + mirror_lights + '&model=' + model
put_url = 'https://developer-api.govee.com/v1/devices/control'
off = {"device": mirror_lights, "model": model, "cmd": {"name": "turn", "value": "off"}}
on = {"device": mirror_lights, "model": model, "cmd": {"name": "turn", "value": "on"}}


while True:
    #mirror_lights_get = requests.get(get_url, headers=key)
    #mirror_lights_json = mirror_lights_get.json()
    #mirror_lights_state = mirror_lights_json['data']['properties'][1]['powerState']
    mirror_url = 'http://192.168.1.163:8080/'
    mirror_get = requests.get(mirror_url)
    mirror_json = mirror_get.json()
    mirror_in_use = str(mirror_json['is_in_use'])
    
    if mirror_in_use == 'True':
        requests.put(put_url, headers=key, json=on)
        print(mirror_in_use)
    else:
        requests.put(put_url, headers=key, json=off)
        print(mirror_in_use)
        
        
    sleep(10)

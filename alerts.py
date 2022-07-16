#!/usr/bin/python3

import requests
import json


alert_list = []
alert_counter = 0
headers = {'User-Agent': '(homeweatherapp, aa.ron.t.stern@gmail.com)'}

try:
    nws_alerts_url = 'https://api.weather.gov/alerts/active/zone/NYZ075
    nws_alerts_get = requests.get(nws_alerts_url, headers=headers)
    try:
        nws_alerts_data = nws_alerts_get.json()
        for _ in nws_alerts_data:
            if nws_alerts_data['features'][alert_counter]['properties']['status'] == 'Test':
                pass
            else:
                alert_headline = nws_alerts_data['features'][alert_counter]['properties']['event']  # .title()
                try:
                    alert_description_full = nws_alerts_data['features'][alert_counter]['properties']['parameters']['NWSheadline'][0]
                except:
                    alert_description_full = ''
                # alert_description_split = alert_description_full.split('\n\n')
                # alert_description = (alert_description_split[0])
                alert_icon = u"\u26A0"
                alert_list.append(alert_icon + ' ' + alert_headline + ' ' + alert_icon + ' ' + alert_description_full)
                alert_counter += 1
    except:
        pass
except IndexError:
    pass
except KeyError:
    pass
alerts = (' '.join(alert_list))
print(alerts)

with open('/home/pi/IpadDisplay/alerts.json', 'w', encoding='utf-8') as f:
    json.dump(alerts, f, ensure_ascii=False, indent=4)

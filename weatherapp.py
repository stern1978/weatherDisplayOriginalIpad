#!/usr/bin/python3

import requests
import json
from flask import Flask, render_template, redirect
from time import sleep


app = Flask(__name__)
app.config.from_object(__name__)

current_data = r'/home/pi/IpadDisplay/current.json'
forecast_data = r'/home/pi/IpadDisplay/forecast.json'
inside_data = r'/home/pi/IpadDisplay/inside.json'
alerts_data = r'/home/pi/IpadDisplay/alerts.json'
url_list = [current_data, forecast_data, inside_data, alerts_data]

@app.route('/')
def index():
    while True:
        try:
            current_url = r'/home/pi/IpadDisplay/current.json'
            with open(current_url) as current:
                current_data = json.load(current)
            forecast_url = r'/home/pi/IpadDisplay/forecast.json'
            with open(forecast_url) as forecast:
                forecast_data = json.load(forecast)
            inside_url = r'/home/pi/IpadDisplay/inside.json'
            with open(inside_url) as inside:
                inside_data = json.load(inside)
            alerts_url = r'/home/pi/IpadDisplay/alerts.json'
            with open(alerts_url) as alert:
                alerts_data = json.load(alert)

            sunrise = current_data['sunrise']
            sunset = current_data['sunset']
            outside_temp = round(current_data['outside_temp'])
            real_feel = round(current_data['real_feel'])
            high = round(current_data['high'])
            low = round(current_data['low'])
            rain_hr = round(current_data['rain_hr'], 2)
            snow_hr = round(current_data['snow_hr'], 2)
            clouds = current_data['clouds']
            icon = current_data['icon']
            humidity = current_data['humidity']
            description = current_data['description']
            inside_temp = inside_data['temp']
            forecast = forecast_data
            alerts = alerts_data
            break
        except json.JSONDecodeError:
            sleep(1)
            index()
        except RecursionError:
            sleep(1)
            index()

    return render_template('weatherapp.html',
                           outsidetemp=outside_temp,
                           realfeel=real_feel,
                           high=high,
                           low=low,
                           rain_hr=rain_hr,
                           snow_hr=snow_hr,
                           sunrise=sunrise,
                           sunset=sunset,
                           clouds=clouds,
                           icon=icon,
                           description=description,
                           avgtemp=inside_temp,
                           forecast=forecast,
                           alerts=alerts,
                           humidity=humidity)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008, debug=True)

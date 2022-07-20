import time
import requests
import json
import datetime
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    weather_url = 'https://api.openweathermap.org/data/2.5/onecall?lat=40.6168729&lon=-74.0362195&units=imperial&appid=6e541b24e86c92513c6df3b8cd983fc8'
    weather_get = requests.get(weather_url)
    weather_data = weather_get.json()

    alerts_url = 'https://api.weatherapi.com/v1/forecast.json?key=82b8064412a8414ca27224745221501&q=40.6168729,%20-74.0362195&days=1&aqi=yes&alerts=yes'
    alerts_get = requests.get(alerts_url)
    alerts_data = alerts_get.json()

    counter = 0
    alertslist = []
    sunrise = datetime.datetime.fromtimestamp(weather_data['current']['sunrise']).strftime('%I:%M %p')
    sunset = datetime.datetime.fromtimestamp(weather_data['current']['sunset']).strftime('%I:%M %p')
    sunrisetomorrow = datetime.datetime.fromtimestamp(weather_data['daily'][1]['sunrise']).strftime('%I:%M %p')
    outsidetemp = round(weather_data['current']['temp'])
    realfeel = round(weather_data['current']['feels_like'])
    high = round(weather_data['daily'][0]['temp']['max'])
    low = round(weather_data['daily'][0]['temp']['min'])
    humidity = weather_data['current']['humidity']
    dew_point = weather_data['current']['dew_point']
    uv = weather_data['current']['uvi']
    cloud_cover = weather_data['current']['clouds']
    description = weather_data['current']['weather'][0]['description'].title()
    icon = '/static/' + weather_data['current']['weather'][0]['icon'] + '.png'
    try:
        rainhr = weather_data['current']['rain']['1h']
    except KeyError:
        rainhr = None
    try:
        snowhr = weather_data['current']['snow']['1h']
    except KeyError:
        snowhr = None

    # Alerts

    try:
        alert = weather_data['alerts']
        for a in alert:
            alertslist.append(a['description'])
            counter += 1

    except KeyError:
        alerts = None
    alerts = (' - - - '.join(alertslist))
    print(alerts)

    # Forecast
    forecastlist = []
    daycounter = 1
    daily = weather_data['daily'][daycounter]
    for k in daily:
        try:
            if daycounter < 4:
                day = datetime.datetime.fromtimestamp(weather_data['daily'][daycounter]['dt']).strftime('%a %d')
                fmax = round(weather_data['daily'][daycounter]['temp']['max'])
                fmin = round(weather_data['daily'][daycounter]['temp']['min'])
                ficon = "/static/" + weather_data['daily'][daycounter]['weather'][0]['icon'] + ".png"
                precip = weather_data['daily'][daycounter]['pop']
                try:
                    rain = round(weather_data['daily'][daycounter]['rain'] / 25.4, 2)
                except KeyError:
                    rain = 0.00
                try:
                    snow = round(weather_data['daily'][daycounter]['snow'] / 25.4 * 10, 2)
                except KeyError:
                    snow = 0.00
                daylist = (day, fmax, fmin, ficon, precip, rain, snow)
                forecastlist.append(daylist)
                daycounter += 1
                print(daylist)

        except IndexError:
            pass

    forcasthourlst = []
    hourcounter = 0
    hourly = weather_data['hourly']
    for h in hourly:
        htime = datetime.datetime.fromtimestamp(hourly[hourcounter]['dt']).strftime('%-I:%M %p')
        hpop = hourly[hourcounter]['pop']
        try:
            hrain = round(hourly[hourcounter]['rain']['1h'])  # / 25.4 ,2)
        except KeyError:
            hrain = 'error'
        try:
            hsnow = round(hourly[hourcounter]['snow']['1h'])  # / 25.4 ,2)
        except KeyError:
            hsnow = 'error'

        hourcounter += 1

    # Inside Temp
    key = 'uF0cIT4Fxu50HpPqyFqtjofmfSMdtWmVg97ZPh7c'  # os.environ.get('HUE_API')
    url = "http://192.168.1.198/api/" + key + "/sensors"
    roomtemp = []
    get = requests.get(url)
    weather_data = get.json()
    for num in weather_data:
        try:
            rawtemp = weather_data[num]['state']['temperature']
            temp = ((rawtemp / 100) * 9 / 5) + 32
            roomtemp.append(temp)
        except KeyError:
            pass
    avgtemp = round(sum(roomtemp) / len(roomtemp))

    return render_template('home_test.html',
                           avgtemp=avgtemp,
                           sunrise=sunrise,
                           sunset=sunset,
                           outsidetemp=outsidetemp,
                           realfeel=realfeel,
                           description=description,
                           icon=icon,
                           alerts=alerts,
                           high=high,
                           low=low,
                           forcast=forecastlist,
                           sunrisetomorrow=sunrisetomorrow,
                           rainhr=rainhr,
                           snowhr=snowhr)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

#import weather
#import inside
import time
import requests
import json
import datetime
from flask import Flask, render_template, request, redirect, jsonify


app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=40.6168729&lon=-74.0362195&units=imperial&appid=6e541b24e86c92513c6df3b8cd983fc8'
    get = requests.get(url)
    data = get.json()
    counter = 0
    alertslist = []
    sunrise = datetime.datetime.fromtimestamp(data['current']['sunrise']).strftime('%I:%M %p')
    sunset = datetime.datetime.fromtimestamp(data['current']['sunset']).strftime('%I:%M %p')
    sunrisetomorrow = datetime.datetime.fromtimestamp(data['daily'][1]['sunrise']).strftime('%I:%M %p')
    outsidetemp = round(data['current']['temp'])
    
    realfeel = round(data['current']['feels_like'])
    high = round(data['daily'][0]['temp']['max'])
    low = round(data['daily'][0]['temp']['min'])
    humidity = data['current']['humidity']
    dew_point = data['current']['dew_point']
    uv = data['current']['uvi']
    cloud_cover = data['current']['clouds']
    description = data['current']['weather'][0]['description'].title()
    icon = '/static/' + data['current']['weather'][0]['icon'] + '.png'
    try:
        rainhr = data['current']['rain']['1h']
    except KeyError:
        rainhr = None
    try:
        snowhr = data['current']['snow']['1h']
    except KeyError:
        snowhr = None
    try:
        alert = data['alerts']
        for a in alert:
            alertslist.append(a['event'])
            counter += 1
    except KeyError:
        alert = None
    alerts = (', '.join(alertslist))

    forcastlst = []
    daycounter = 0
    forcastday = data['daily'][daycounter]
    for k in forcastday:
        try:
            day = datetime.datetime.fromtimestamp(data['daily'][daycounter]['dt']).strftime('%a %d')
            fmax = round(data['daily'][daycounter]['temp']['max'])
            fmin = round(data['daily'][daycounter]['temp']['min'])
            ficon = "/static/" + data['daily'][daycounter]['weather'][0]['icon'] + ".png"
            precip = data['daily'][daycounter]['pop']
            try:
                rain = round(data['daily'][daycounter]['rain'] / 25.4 ,2)
            except KeyError:
                rain = 0
            try:
                snow = round(data['daily'][daycounter]['snow'] / 25.4 ,2)
            except KeyError:
                snow = 0
            #daylist = {"day":day, "max":fmax, "min":fmin, "icon":ficon, "precip":precip, "rain":rain, "snow":snow}
            daylist = (day, fmax, fmin, ficon, precip, rain, snow)
            forcastlst.append(daylist)
            daycounter += 1
            
        except IndexError:
            pass
        
    key = 'uF0cIT4Fxu50HpPqyFqtjofmfSMdtWmVg97ZPh7c'  # os.environ.get('HUE_API')
    url = "http://192.168.1.198/api/" + key + "/sensors"
    roomtemp = []
    get = requests.get(url)
    data = get.json()
    for num in data:
        try:
            rawtemp = data[num]['state']['temperature']
            temp = ((rawtemp / 100) * 9 / 5) + 32
            roomtemp.append(temp)
        except KeyError:
            pass
    avgtemp = round(sum(roomtemp)/len(roomtemp))
    print(temp)

    return render_template('home.html',
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
                           forcast=forcastlst,
                          sunrisetomorrow=sunrisetomorrow)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
    
import time
import requests
import json
import datetime
from flask import Flask, render_template, request, redirect, jsonify


app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    url = 'http://api.weatherapi.com/v1/forecast.json?key=82b8064412a8414ca27224745221501&q=40.6168729,%20-74.0362195&days=5&aqi=yes&alerts=yes'
    get = requests.get(url)
    data = get.json()
    counter = 0
    alertslist = []
    #sunrise = datetime.datetime.fromtimestamp(data['current']['sunrise']).strftime('%I:%M %p')
    #sunset = datetime.datetime.fromtimestamp(data['current']['sunset']).strftime('%I:%M %p')
    #sunrisetomorrow = datetime.datetime.fromtimestamp(data['daily'][1]['sunrise']).strftime('%I:%M %p')
    outsidetemp = round(data['current']['temp_f'])
    realfeel = round(data['current']['feelslike_f'])
    high = round(data['forecast']['forecastday'][0]['day']['maxtemp_f'])
    low = round(data['forecast']['forecastday'][0]['day']['mintemp_f'])
    #humidity = data['current']['humidity']
    #dew_point = data['current']['dew_point']
    #uv = data['current']['uvi']
    #cloud_cover = data['current']['clouds']
    description = data['current']['condition']['text'].title()
    icon = data['current']['condition']['icon']

    '''try:
        rainhr = data['current']['rain']['1h']
    except KeyError:
        rainhr = None
    try:
        snowhr = data['current']['snow']['1h']
    except KeyError:
        snowhr = None'''
    
    # Alerts
    try:
        alert = data['alerts']['alert']
        for a in alert:
            #print(a)
            if 'Kings (Brooklyn)' in a['areas']:
                alertslist.append(' ... ' + a['headline'])
            else:
                pass
            counter += 1
    except KeyError:
        alert = None
    alerts = (''.join(alertslist))
    print(alerts)
    
    # Forcast
    forcastlst = []
    daycounter = 0
    for k in data['forecast']['forecastday']:
        try:
            epoch = (data['forecast']['forecastday'][daycounter]['date_epoch']+18000)
            day = datetime.datetime.fromtimestamp(epoch).strftime('%a %d')
            fmax = round(data['forecast']['forecastday'][daycounter]['day']['maxtemp_f'])
            fmin = round(data['forecast']['forecastday'][daycounter]['day']['mintemp_f'])
            ficon = data['forecast']['forecastday'][daycounter]['day']['condition']['icon']
            try:
                rain = round(data['forecast']['forecastday'][daycounter]['day']['daily_chance_of_rain'])
            except KeyError:
                rain = 0.00
            try:
                snow = round(data['forecast']['forecastday'][daycounter]['day']['daily_chance_of_snow'])
            except KeyError:
                snow = 0.00
            daylist = (day, fmax, fmin, ficon, rain, snow)
            forcastlst.append(daylist)
            daycounter += 1
            print(epoch, day, forcastlst)
            
        except IndexError:
            pass
    
    '''forcasthourlst = []
    hourcounter = 0
    hourly = data['hourly']
    for h in hourly:
        htime = datetime.datetime.fromtimestamp(hourly[hourcounter]['dt']).strftime('%-I:%M %p')
        hpop = hourly[hourcounter]['pop']
        try:
            hrain = round(hourly[hourcounter]['rain']['1h'])# / 25.4 ,2)
        except KeyError:
            hrain = 'error'
        try:
            hsnow = round(hourly[hourcounter]['snow']['1h'])# / 25.4 ,2)
        except KeyError:
            hsnow = 'error'       
        
        
        hourcounter += 1
    
        #print(hourcounter, htime, hpop, hrain, hsnow)'''
    
    # Inside Temp
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

    return render_template('home_test1.html',
                           avgtemp=avgtemp,
                           outsidetemp=outsidetemp,
                           realfeel=realfeel,
                           description=description,
                           icon=icon,
                           alerts=alerts,
                           high=high,
                           low=low,
                           forcast=forcastlst)#,
                          #rainhr=rainhr,
                          #snowhr=snowhr)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
    
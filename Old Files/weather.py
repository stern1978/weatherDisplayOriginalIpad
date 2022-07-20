import requests
import json
import time
import datetime


def outside():
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=40.6168729&lon=-74.0362195&units=imperial&appid=6e541b24e86c92513c6df3b8cd983fc8'
    get = requests.get(url)
    data = get.json()
    counter = 0
    alertslist = []
    sunrise = datetime.datetime.fromtimestamp(data['current']['sunrise']).strftime('%I:%M %p')
    sunset = datetime.datetime.fromtimestamp(data['current']['sunset']).strftime('%I:%M %p')
    sunrisetomorrow = datetime.datetime.fromtimestamp(data['daily'][1]['sunrise']).strftime('%I:%M %p')
    temp = round(data['current']['temp'])
    feels_like = round(data['current']['feels_like'])
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
            daylist = (day, fmax, fmin, ficon, precip, rain, snow)
            forcastlst.append(daylist)
            daycounter += 1
            
        except IndexError:
            pass
        
    return (sunrise,
            sunset,
            temp,
            feels_like,
            humidity,
            dew_point,
            uv,
            cloud_cover,
            description,
            icon,
            alerts,
            high,
            low,
            forcastlst,
            rainhr,
            snowhr,
           sunrisetomorrow)


if __name__ == "__main__":
    outside()

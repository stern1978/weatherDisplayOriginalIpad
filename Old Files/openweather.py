import requests
import datetime
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)
headers = {'User-Agent': '(homeweatherapp, aa.ron.t.stern@gmail.com)'}


@app.route('/')
def index():
    weather_url = 'https://api.openweathermap.org/data/2.5/onecall?lat=40.6168729&lon=-74.0362195&units=imperial&appid=6e541b24e86c92513c6df3b8cd983fc8'
    weather_get = requests.get(weather_url)
    weather_data = weather_get.json()

    # Current
    sunrise = datetime.datetime.fromtimestamp(weather_data['current']['sunrise']).strftime('%I:%M %p')
    sunset = datetime.datetime.fromtimestamp(weather_data['current']['sunset']).strftime('%I:%M %p')
    sunrise_tomorrow = datetime.datetime.fromtimestamp(weather_data['daily'][1]['sunrise']).strftime('%I:%M %p')
    outside_temp = round(weather_data['current']['temp'])
    real_feel = round(weather_data['current']['feels_like'])
    high = round(weather_data['daily'][0]['temp']['max'])
    low = round(weather_data['daily'][0]['temp']['min'])
    try:
        rain = round(weather_data['daily'][0]['rain'] / 25.4, 2)
    except KeyError:
        rain = 0.00
    try:
        if outside_temp in range(28, 35):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 10, 2)
        elif outside_temp in range(20, 28):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 15, 2)
        elif outside_temp in range(15, 20):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 20, 2)
        elif outside_temp in range(10, 15):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 30, 2)
        elif outside_temp in range(0, 10):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 40, 2)
        elif outside_temp in range(-20, 0):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 50, 2)
        elif outside_temp in range(-100, -20):
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 100, 2)
        else:
            snow = round(weather_data['daily'][0]['snow'] / 25.4 * 1, 2)
    except KeyError:
        snow = 0.00
    # humidity = weather_data['current']['humidity']
    # dew_point = weather_data['current']['dew_point']
    # uv = weather_data['current']['uvi']
    # cloud_cover = weather_data['current']['clouds']
    description = weather_data['current']['weather'][0]['description'].title()
    icon = '/static/' + weather_data['current']['weather'][0]['icon'] + '.png'

    try:
        rain_hr = round(weather_data['current']['rain']['1h'] / 25.4, 2)
    except KeyError:
        rain_hr = 0.00
    try:
        if outside_temp in range(28, 35):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 10, 2)
        elif outside_temp in range(20, 28):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 15, 2)
        elif outside_temp in range(15, 20):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 20, 2)
        elif outside_temp in range(10, 15):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 30, 2)
        elif outside_temp in range(0, 10):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 40, 2)
        elif outside_temp in range(-20, 0):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 50, 2)
        elif outside_temp in range(-100, -20):
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 100, 2)
        else:
            snow_hr = round(weather_data['current']['snow']['1h'] / 25.4 * 1, 2)
    except KeyError:
        snow_hr = 0.00

    # Alerts
    alert_list = []
    alert_counter = 0
    try:
        nws_alerts_url = 'https://api.weather.gov/alerts/active/zone/NYZ075'  # 'https://api.weather.gov/alerts/active?point=40.6168364,-74.0361376'  # https://api.weather.gov/alerts/active?zone=NYZ075'
        nws_alerts_get = requests.get(nws_alerts_url, headers=headers)
        try:
            nws_alerts_data = nws_alerts_get.json()
            for _ in nws_alerts_data:
                alert_headline = nws_alerts_data['features'][alert_counter]['properties']['event']  # .title()
                alert_description_full = nws_alerts_data['features'][alert_counter]['properties']['description']
                # alert_description_split = alert_description_full.split('\n\n')
                # alert_description = (alert_description_split[0])
                alert_icon = u"\u26A0"
                alert_list.append(alert_icon + '   ' + alert_headline + ' ' + alert_icon + alert_description_full)
                alert_counter += 1
        except:
            pass
    except IndexError:
        pass
    except KeyError:
        pass
    alerts = (' '.join(alert_list))

    # Daily Forecast
    forecast_list = []
    day_counter = 1
    daily = weather_data['daily'][day_counter]
    try:
        for _ in daily:
            if day_counter < 6:
                forecast_day = datetime.datetime.fromtimestamp(weather_data['daily'][day_counter]['dt']).strftime(
                    '%a %d')
                forecast_max = round(weather_data['daily'][day_counter]['temp']['max'])
                forecast_min = round(weather_data['daily'][day_counter]['temp']['min'])
                forecast_icon = "/static/" + weather_data['daily'][day_counter]['weather'][0]['icon'] + ".png"
                forecast_description = weather_data['daily'][day_counter]['weather'][0]['description']
                forecast_pop = weather_data['daily'][day_counter]['pop']
                avg_temp = (forecast_max + forecast_min) / 2
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
                day_list = (forecast_day, forecast_max, forecast_min, forecast_icon, forecast_pop, forecast_rain, forecast_snow)
                forecast_list.append(day_list)
                day_counter += 1

    except IndexError:
        pass

    # Inside Temp
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
    avg_temp = round(sum(room_temp) / len(room_temp))

    return render_template('openweather.html',
                           avgtemp=avg_temp,
                           sunrise=sunrise,
                           sunset=sunset,
                           outsidetemp=outside_temp,
                           realfeel=real_feel,
                           description=description,
                           icon=icon,
                           alerts=alerts,
                           high=high,
                           low=low,
                           forcast=forecast_list,
                           sunrisetomorrow=sunrise_tomorrow,
                           rainhr=rain_hr,
                           snowhr=snow_hr,
                           rain=rain,
                           snow=snow)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

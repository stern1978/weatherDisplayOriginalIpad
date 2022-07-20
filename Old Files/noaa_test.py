import requests
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)
headers = {'User-Agent': '(homeweatherapp, aa.ron.t.stern@gmail.com)'}


@app.route('/')
def index():
    noaa_latest_url = 'https://api.weather.gov/stations/KEWR/observations/latest'
    noaa_latest_get = requests.get(noaa_latest_url, headers=headers)
    noaa_latest_data = noaa_latest_get.json()

    noaa_forecast_url = 'https://api.weather.gov/gridpoints/OKX/32,29/forecast'
    noaa_forecast_get = requests.get(noaa_forecast_url, headers=headers)
    noaa_forecast_data = noaa_forecast_get.json()

    noaa_alerts_url = 'https://api.weather.gov/alerts/active?point=40.6168364,-74.0361376'
    noaa_alerts_get = requests.get(noaa_alerts_url, headers=headers)
    noaa_alerts_data = noaa_alerts_get.json()

    # Current
    outside_temp = round((noaa_latest_data['properties']['temperature']['value'] * 9 / 5) + 32)
    wind_chill = noaa_latest_data['properties']['windChill']['value']
    heat_index = noaa_latest_data['properties']['heatIndex']['value']
    if wind_chill is not None:
        real_feel = round((wind_chill * 9 / 5) + 32)
    elif heat_index is not None:
        real_feel = round((heat_index * 9 / 5) + 32)
    else:
        real_feel = outside_temp
    icon = noaa_latest_data['properties']['icon']
    text_description = noaa_latest_data['properties']['textDescription']
    day_detailed_forecast = noaa_forecast_data['properties']['periods'][0]['detailedForecast']

    # Alerts
    alert_list = []
    alert_counter = 0

    try:
        alert = noaa_alerts_data
        for _ in alert:
            try:
                alert_headline = alert['features'][alert_counter]['properties']['headline']
                alert_description = alert['features'][alert_counter]['properties']['description']
                alert_list.append(alert_headline + ' . . . ' + alert_description)
                alert_counter += 1
            except KeyError:
                pass
    except IndexError:
        pass
    alerts = (' - - - '.join(alert_list))

    # Daily Forecast
    forecast_list = []
    day_counter = 0
    daily_forecast = noaa_forecast_data['properties']['periods']
    temp_trend_today = daily_forecast[0]['temperatureTrend']
    if temp_trend_today is None:
        temp_trend = 'Steady'
    else:
        temp_trend = temp_trend_today.capitalize()
    for _ in daily_forecast:
        if day_counter < 6:
            forecast_day = (daily_forecast[day_counter]['name'])
            forecast_temp = daily_forecast[day_counter]['temperature']
            forecast_trend = daily_forecast[day_counter]['temperatureTrend']
            forecast_icon = daily_forecast[day_counter]['icon']
            day_list = (forecast_day, forecast_temp, forecast_trend, forecast_icon)
            forecast_list.append(day_list)
            day_counter += 1

    # Inside Temp
    key = 'uF0cIT4Fxu50HpPqyFqtjofmfSMdtWmVg97ZPh7c'  # os.environ.get('HUE_API')
    noaa_latest_url = "http://192.168.1.151/api/" + key + "/sensors"
    room_temp = []
    noaa_latest_get = requests.get(noaa_latest_url)
    weather_data = noaa_latest_get.json()
    for num in weather_data:
        try:
            raw_temp = weather_data[num]['state']['temperature']
            temp = ((raw_temp / 100) * 9 / 5) + 32
            room_temp.append(temp)
        except KeyError:
            pass
    avg_temp = round(sum(room_temp) / len(room_temp))

    return render_template('noaa_test.html',
                           avgtemp=avg_temp,
                           outsidetemp=outside_temp,
                           dayforecast=day_detailed_forecast,
                           realfeel=real_feel,
                           icon=icon,
                           textDescription=text_description,
                           temp_trend=temp_trend,
                           alerts=alerts,
                           forcast=forecast_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)

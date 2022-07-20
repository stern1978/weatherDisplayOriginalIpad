import os
import requests
import time
import json

key = 'uF0cIT4Fxu50HpPqyFqtjofmfSMdtWmVg97ZPh7c'  # os.environ.get('HUE_API')
url = "http://192.168.1.198/api/" + key + "/sensors"


roomtemp = []

def temp():
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
    print(avgtemp)

    return (avgtemp)


if __name__ == "__main__":
    temp()

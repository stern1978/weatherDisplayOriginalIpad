#!/usr/bin/python3

import requests
import json
from money import get_sheets_service as sh
from flask import Flask, render_template, redirect
from time import sleep

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    laundry_list = sh()
    print(laundry_list)
    return render_template('laundry.html',
                            laundry_list=laundry_list)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)

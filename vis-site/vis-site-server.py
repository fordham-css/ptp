from flask import Flask, render_template

import json
import plotly

import requests

path = 'http://127.0.0.1:5000/'

def get_data(url):
    r = requests.get(url+'api/last_row')
    return r.text

def loop_get():
    while True:
        get_data(path)

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():

    return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True,port=4000)
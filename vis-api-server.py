from flask import Flask, url_for, json
from flask import request, jsonify
from functools import wraps
import time
import sys
import datetime
app = Flask(__name__)

import logging
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


from utils import *
import redis

r = redis.Redis(host='localhost',port=6669)
r.set_response_callback('SMEMBERS', list)

stock = sys.argv[1]

@app.route('/api/last_row', methods = ['GET'])
def last_row():
    
    # Make timestamp
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    # Log init request
    app.logger.info('[+] [' + timestamp + '] ' + 'GET request recieved.')
    
    # Prepare bot response
    #therapy(parse_user_says(user_says))
    
    row = get_range_row(stock,-1,-1,r)[0]
    
    return jsonify({'stock':stock,'stamp':row[0],'price':row[1],'bid':row[2],'ask':row[3]})
 
if __name__ == '__main__':
	app.run(debug=True,port=5000)
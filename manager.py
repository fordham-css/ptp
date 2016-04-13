########################################
# MANAGER.py
# Runs gather, hunter, killer procs
# Runs databse
# Does everything TBH
########################################

from utils import *
import redis
import sys
import os

# Import  threading functionality 
import threading

# Connect to redis instance
print '[+] Connecting to database on port 6669...'
r = redis.Redis(host='localhost',port=6669)
r.set_response_callback('SMEMBERS', list)
print '[+] Database connected..'

# Flush redis instance db
print '[+] Flushing database on port 6669...'
is_flushed = flush()
print '[+] Database flushed: %s' % is_flushed

# Get stock from command line
if len(sys.argv) == 2:
    stock=str(sys.argv[1].upper())
# Get stock to target from HUNTER
else:
    print '[+] Getting stock from HUNTER.py...'
    stock=hunter()
print '[+] Stock selected: %s' % stock

# Get run
run = 1
try:
    if len(get_range_row(stock,0,0,r)) > 1:
        r += 1
except:
    print '[+] Run %s on %s' % (run,stock)
    
# Start streaming data from GATHER
print '[+] Beginning Gather loop'
def start_gather():
    loop_gather(stock)
gather_thread = threading.Thread(target=start_gather)
gather_thread.start()
print '[+] Gather running...'

import time
time.sleep(5)

# Begin Buy run
ask_gap = .02
print '[+] Ask gap set at %s' % ask_gap
print '[+] Commencing BUY LOOP...'
bought_at = buy(stock,ask_gap,r)[1]
print 'Bought %s at %s' % (stock,bought_at)

# Save DB data
print '[+] Saving DB data to csv at ./data/...'
os.system('python db-csv.py %s %s' % (run, stock))
print '[+] File saved.'

# Begin Sell run
risk_appetite = 2000
risk_appetite_slope = 1
recovery_appetite = 100
print '[+] Risk appetite set at %s observations' % risk_appetite
print '[+] Commencing SELL LOOP...'
sold_at = sell(stock,bought_at,risk_appetite,risk_appetite_slope,recovery_appetite,r)[1]
print 'Sold %s at %s' % (stock,sold_at[1])

# Save DB data
print '[+] Saving DB data to csv at ./data/...'
os.system('python db-csv.py %s %s' % (run, stock))
print '[+] File saved.'

# Flush redis instance db
print '[+] Flushing database on port 6669...'
is_flushed = flush()
print '[+] Database flushed: %s' % is_flushed

# End GATHER Thread
gather_thread.stop()

# End Redis Thread
#redis_thread.stop()
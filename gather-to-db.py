##############################################
# gather-to-db.py
# gathers for a set amount to the db
# usage: python gather-to-db.py STOCK 100
##############################################
import sys
from utils import *
def gather_to_db(stock,lim):   
    import redis

    r = redis.Redis(host='localhost',port=6669)
    r.set_response_callback('SMEMBERS', list)



    gather(stock,1)
    for each in range(lim):
        gather(stock,(each+1))

gather_to_db(sys.argv[1].upper(),int(sys.argv[2]))

#os.system('./redis-1.2.5/redis-server ./redis-1.2.5/redis.conf')
"""
get_from_db(1,stock,r)
os.system('pkill "redis-server"')
"""
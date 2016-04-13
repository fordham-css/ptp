##############################################
# download-db-csv.py
# downloads everything on the database to csv
# usage: python download-db-csv.py 1 STOCK 
##############################################
import sys
from utils import *
def download_db_csv(run,stock):
    
    import redis

    r = redis.Redis(host='localhost',port=6669)
    r.set_response_callback('SMEMBERS', list)

    get_from_db(run,stock,r)

download_db_csv(int(sys.argv[1]),sys.argv[2].upper())
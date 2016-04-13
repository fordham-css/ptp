##########################################
# UTILS.py
# Helper functions for calculating & more
# For use in main and other programs
##########################################

from hunter import hunter
from gather import gather
from killer import buy, sell

def loop_gather(stock):
    count = 1
    while True:
        gather(stock,count)
        count += 1

def flush():
    import redis
    r = redis.Redis(host='localhost',port=6669)
    r.flushall()
    r.flushdb()
    return True

# get all rows
def get_all_row(stock,r):
    import ast
    tmp=[]
    for each in list(r.zrange(stock,0,-1,desc=False, withscores=False)):
        tmp.append(ast.literal_eval(each)) 
    return tmp

# get all columns
def get_all_col(stock,r,column):
    import ast
    tmp=[]
    for each in list(r.zrange(stock,0,-1,desc=False, withscores=False)):
        tmp.append(ast.literal_eval(each)[column]) 
    return tmp

# get a range of rows
def get_range_row(stock,start,end,r):
    import ast
    tmp=[]
    for each in list(r.zrange(stock,start,end,desc=False, withscores=False)):
        tmp.append(ast.literal_eval(each)) 
    return tmp
    
# get a range of col
def get_range_col(stock,start,end,r,column):
    import ast
    tmp=[]
    for each in list(r.zrange(stock,start,end,desc=False, withscores=False)):
        tmp.append(ast.literal_eval(each)[column]) 
    return tmp
    
# get last timestamp
def last_stamp(stock,r):
    import ast
    return ast.literal_eval(list(r.zrange(stock,-1,-1,desc=False, withscores=False))[0])[0]
  
# get last traded price  
def last_trade(stock,r):
    import ast
    return ast.literal_eval(list(r.zrange(stock,-1,-1,desc=False, withscores=False))[0])[1]

# get last ask price    
def last_ask(stock,r):
    import ast
    return ast.literal_eval(list(r.zrange(stock,-1,-1,desc=False, withscores=False))[0])[2]

# get last bid price    
def last_bid(stock,r):
    import ast
    return ast.literal_eval(list(r.zrange(stock,-1,-1,desc=False, withscores=False))[0])[3]

# get col
def col(matrix, i):
    return [int(row[i]) for row in matrix]

# get average of a list     
def avg(alist): 
    return sum(alist)/float(len(alist))

# get slope of a list
def get_slope(alist):
    return (alist[-1] - alist[0])/float(len(alist))

# get standard deviation
def get_sd(alist,avg):
    from math import sqrt
    bin = 0.0
    sd = 0.0
    for each in alist:
        bin += (each-avg)*(each-avg)
    return sqrt(bin/float(len(alist)))

# get sd list
def sd_get_list(stock,r,number):
    price_list = []
    for each in range(number):
        current = (each+1)*(-1)
        histor = (number-each)*(-1)
        price_list.append(get_range_row(stock,histor,histor,r)[0][1])
    
    
    sd_list = []
    for each in range(number):
        x=each+1
        sd_list.append(get_sd(price_list[0:x],avg(price_list[0:x])))
    
    #return sd_list
    return sd_list

# get slope of average 
def get_sla(alist):
    return (avg(alist) - alist[0])/float(len(alist))

# get sla list
def sla_get_list(stock,r,number):
    price_list = []
    for each in range(number):
        current = (each+1)*(-1)
        histor = (number-each)*(-1)
        price_list.append(get_range_row(stock,histor,histor,r)[0][1])
    
    
    sd_list = []
    for each in range(number):
        x=each+1
        sd_list.append(get_sd(price_list[0:x],avg(price_list[0:x])))

# how many negative?
def neg_count(alist):
    count = 0
    for each in alist:
        if each < 0.00000000000000000000000000000000000000000000000:
            count += 1
    
    return count
   

# save DB to CSV
def get_from_db(run,stock,r):

    rows = get_all_row(stock,r)

    first_time = rows[0][0][0:19]

    with open('data/%s-%s-at-%s.csv' % (run,stock,first_time), 'w+') as f:
        f.write('time,price,bid,ask\n')
        f.close()
        
    with open('data/%s-%s-at-%s.csv' % (run,stock,first_time), 'a') as f:
        for each in rows:
            f.write("%s,%s,%s,%s\n" % (each[0],each[1],each[2],each[3]))
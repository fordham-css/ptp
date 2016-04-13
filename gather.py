########################################
# GATHER.py
# Grabs financial data from Robinhood
# Save to Redis servis at port 6669
########################################



def gather(stock,count):

    # import the robinhood api library
    from Robinhood import Robinhood
    import os
    import time
    import datetime
    


    #key setup
    import ast
    keys =[]
    f = open('keys')
    keys = ast.literal_eval(f.read())
    f.close()
    
    # login
    ## log into robinhood
    my_trader = Robinhood();
    my_trader.login(username=keys[0][1], password=keys[1][1])

    # stock selection
    ## the variable 'stock' is a string passed through the function
    #stock = sys.argv[1].upper()
    stock = stock.upper()
    stock_instrument = my_trader.instruments(stock)[0]

    # variable declaration
    last_trade = 0
    bid_price = 0
    ask_price = 0
    #count = 1
    #sell_prices = []
    #sell_price_slope = 0
    #sell_average_prices = []
    #sell_slope_of_averages = 0
    #sell_sd = []
    #sell_sum = 0
    
    # make timestamp
    stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    #stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%S.%f')
    
    # set up quote data
    quote_data = my_trader.quote_data(stock)
    last_trade = float(quote_data['last_trade_price'])
    bid_price = float(quote_data['bid_price'])
    ask_price = float(quote_data['ask_price'])
    
    payload = [stamp,last_trade,ask_price,bid_price]
   
    # push to redis
    import redis
    r_server = redis.Redis(host='localhost',port=6669)
    r_server.zadd(stock, payload, count)

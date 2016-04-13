########################################
# KILLER.py
# Grabs data from Redis datanase
# Buys and sells based on data
########################################



def buy(stock,ask_gap,r):
    from utils import *
    
    import redis

    r = redis.Redis(host='localhost',port=6669)
    r.set_response_callback('SMEMBERS', list)
    
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

    # config robinhood to trade on that stock
    stock_instrument = my_trader.instruments(stock)[0]

    ############################
    # BUY LOOP
    ############################

    # average and slope declaration
    count = 1
    buy_prices = []
    buy_price_slope = 0
    buy_average_prices = []
    buy_slope_of_averages = 0
    buy_sum = 0

    ## begin buy loop
    buy = False
    bought_at = 0.0
    while buy == False:
        if (last_bid(stock,r)-last_ask(stock,r)) > ask_gap:
            
            
            # buy a single share of the stock at the ask price
            #buy_order = my_trader.place_buy_order(stock_instrument, 1, ask_price)

            # break the buy loop
            buy = True
            bought_at=last_ask(stock,r)
            return buy,bought_at 

def sell(stock,bought_at,risk_appetite,risk_appetite_slope,recovery_appetite,r):

    from utils import *
    
    import redis

    r = redis.Redis(host='localhost',port=6669)
    r.set_response_callback('SMEMBERS', list)
   
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

    sold_at = 0.0
    sell = False
    while sell == False:

        # SELL IF SLOPE OF AVERAGES IS DORPPING TO BELOW .02
        # Need to determine optimal minimum count
        
        ##########################################################################
        # Selling conditions
        ##########################################################################
        # If current price is less than our bought at threshold, sell.
        # If the current price is stagnant for n number of obs, sell.
        # If the current price is descending and cannot recover peak gain, sell.
        ##########################################################################
        
        # FIRST CONDITION: Price floor
        # Is the price at a point where we are breaking even, at verge of a loss
        if last_ask(stock,r) <= (bought_at + 0.03):
            # sell single share at bid_price
            #sell_order = my_trader.place_sell_order(stock_instrument, 1, last_bid(stock,r))
            sell = True
            sold_at=last_bid(stock,r)
        
        # SECOND CONDITION: Stagnancy
        # Is the stock varying around the same small window for a period of obs?
        elif get_slope(sd_get_list(stock,r,risk_appetite)) <= (risk_appetite_slope/risk_appetite):
            # sell single share at bid_price
            #sell_order = my_trader.place_sell_order(stock_instrument, 1, last_bid(stock,r))
            sell = True
            sold_at=last_bid(stock,r)
        
        # THIRD CONDITION: Gains and recovery
        # Is the stock varying around the same small window for a period of obs?
        elif (neg_count(sla_get_list(stock,r,recovery_appetite))+1) >= recovery_appetite:
            # sell single share at bid_price
            #sell_order = my_trader.place_sell_order(stock_instrument, 1, last_bid(stock,r))
            sell = True
            sold_at=last_bid(stock,r)
        
        '''
        # Conservative track
        max_loss = (last_ask(stock,r) - bought_at)/last_ask(stock,r)/2
        if last_ask(stock,r) <= last_ask(stock,r) - (last_ask(stock,r)*max_loss):
        
        # Risk-attracted approach
        if get_sla(get_all_col(stock,r,2)) > 0.0001 and len(get_all_row(stock,r)) > risk_appetite:
            # sell single share at bid_price
            #sell_order = my_trader.place_sell_order(stock_instrument, 1, bid_price)
            sell = True
            sold_at=bid_price
        '''
        
    return sell, sold_at 
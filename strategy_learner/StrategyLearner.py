"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			 	 	 		 		 	  		   	  			  	
Atlanta, Georgia 30332 			  		 			 	 	 		 		 	  		   	  			  	
All Rights Reserved 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Template code for CS 4646/7646 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			 	 	 		 		 	  		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			 	 	 		 		 	  		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			 	 	 		 		 	  		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			 	 	 		 		 	  		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			 	 	 		 		 	  		   	  			  	
or edited. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			 	 	 		 		 	  		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			 	 	 		 		 	  		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			 	 	 		 		 	  		   	  			  	
GT honor code violation. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
-----do not edit anything above this line--- 			  		 			 	 	 		 		 	  		   	  			  	

Student Name: Martin Mathew (replace with your name)
GT User ID: mmathew32 (replace with your User ID)
GT ID: 903241329 (replace with your GT ID)
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt
from datetime import timedelta
import pandas as pd
import util as ut 			  		 			 	 	 		 		 	  		   	  			  	
import random

from indicators import *
from QLearner import QLearner
from marketsimcode import compute_portvals


def author(self):
    return "mmathew32"

class StrategyLearner(object):

    def author(self):
        return "mmathew32"
 			  		 			 	 	 		 		 	  		   	  			  	
    # constructor 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, verbose = False, impact=0.0): 			  		 			 	 	 		 		 	  		   	  			  	
        self.verbose = verbose 			  		 			 	 	 		 		 	  		   	  			  	
        self.impact = impact

    def get_discritized_indicator(self,prices_df,sd):
        bb = get_bollinger_band(prices_df)[sd:]
        rsi = get_rsi(prices_df)[sd:]
        macd = calculate_macd(prices_df)[sd:]
        return (pd.DataFrame(index=bb.index,columns=bb.columns,data=pd.qcut(x=bb.ix[:,0].tolist(),q=10,labels=False,duplicates='drop')),\
                pd.DataFrame(index=rsi.index,columns=rsi.columns,data=pd.qcut(x=rsi.ix[:,0].tolist(),q=10,labels=False,duplicates='drop')),\
                pd.DataFrame(index=macd.index,columns=macd.columns,data=pd.qcut(x=macd.ix[:,0].tolist(),q=10,labels=False,duplicates='drop')))


    def get_price_df(self,dates, symbols):
        price_df = ut.get_data(symbols, dates)
        price_df = price_df / price_df.ix[0]
        price_df.fillna(method='ffill', inplace=True)
        price_df.fillna(method='bfill', inplace=True)
        return price_df
 			  		 			 	 	 		 		 	  		   	  			  	
    # this method should create a QLearner, and train it for trading 			  		 			 	 	 		 		 	  		   	  			  	
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # add your code to do learning here 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # example usage of the old backward compatible util function 			  		 			 	 	 		 		 	  		   	  			  	
        syms=[symbol]

        dates = pd.date_range(sd - timedelta(days=30), ed)
        prices_all = self.get_price_df(dates,syms)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        (bb,rsi,macd) = self.get_discritized_indicator(prices,sd)
        prices = prices[sd:]
        self.q_learner = QLearner(num_states=1000,num_actions=3)

        minCount = 5
        maxCount = 15
        prev_cr =  -10.0

        while True:
            minCount -= 1
            maxCount -= 1
            orders_df = pd.DataFrame(index=prices.index, columns=[symbol])
            prices_iter = prices.iterrows()

            curr_holding = 0
            index , row  = next(prices_iter)

            state = self.get_state_for_indicators(bb.ix[index][symbol], rsi.ix[index][symbol], macd.ix[index][symbol])
            action = self.q_learner.querysetstate(state,training=True)

            trade = self.calculate_trade(curr_holding,action)
            orders_df.ix[index][symbol] = trade
            curr_holding += trade

            prev_row = row
            for index, row in prices_iter:
                reward = (row[symbol] - prev_row[symbol])*curr_holding
                action = self.q_learner.query(state,reward)
                trade = self.calculate_trade(curr_holding, action)
                orders_df.ix[index][symbol] = trade
                curr_holding += trade
                prev_row = row
                state = self.get_state_for_indicators(bb.ix[index][symbol], rsi.ix[index][symbol],
                                                      macd.ix[index][symbol])
            port_vals = compute_portvals(orders_df,symbol,sv,0,impact=self.impact)
            cr = self.get_cumulative_returns(port_vals)
            if (abs(prev_cr - cr[0]) < 0.00001 and minCount < 0) or maxCount < 0 :
                print "Learner Return {}".format(cr[0])
                break
            prev_cr = cr[0]

    def get_cumulative_returns(self,port_val):
        return port_val.ix[-1] / port_val.ix[0] - 1

    def get_action(self,act):
        if act == 0:
            return 'B'
        elif act == 1:
            return 'S'
        elif act == 2:
            return 'N'
        else:
            raise ValueError("Invalid Action")

    def calculate_trade(self, curr_holding, act):
        sell_buy = self.get_action(act)
        if curr_holding == 0 and sell_buy == 'B':
            return 1
        elif curr_holding == 0 and sell_buy == 'S':
            return -1
        elif curr_holding == 1 and sell_buy == 'B':
            return 0
        elif curr_holding == 1 and sell_buy == 'S':
            return -2
        elif curr_holding == -1 and sell_buy == 'B':
            return 2
        elif curr_holding == -1 and sell_buy == 'S':
            return 0
        elif sell_buy == 'N':
            return 0

    def get_state_for_indicators(self, bb, rsi, macd):
         return int(bb*100 + rsi*10 +macd)


    # this method should use the existing policy and test it against new data 			  		 			 	 	 		 		 	  		   	  			  	
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        syms=[symbol]

        dates = pd.date_range(sd - timedelta(days=50), ed)
        prices_all = self.get_price_df(dates, syms)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        (bb, rsi, macd) = self.get_discritized_indicator(prices, sd - timedelta(days=22))
        prices = prices[sd:]

        orders_df = pd.DataFrame(index=prices.index, columns=[symbol])
        prices_iter = prices.iterrows()

        curr_holding = 0
        index, row = next(prices_iter)

        state = self.get_state_for_indicators(bb.ix[index][symbol], rsi.ix[index][symbol], macd.ix[index][symbol])
        action = self.q_learner.querysetstate(state)

        trade = self.calculate_trade(curr_holding,action)
        orders_df.ix[index][symbol] = trade
        curr_holding += trade

        prev_row = row
        for index, row in prices_iter:
            action = self.q_learner.querysetstate(state)
            trade = self.calculate_trade(curr_holding, action)
            orders_df.ix[index][symbol] = trade
            curr_holding += trade
            prev_row = row
            state = self.get_state_for_indicators(bb.ix[index][symbol], rsi.ix[index][symbol],
                                                  macd.ix[index][symbol])
        return orders_df



    def testPolicy_ret_action(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        syms=[symbol]

        dates = pd.date_range(sd - timedelta(days=50), ed)
        prices_all = self.get_price_df(dates, syms)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        (bb, rsi, macd) = self.get_discritized_indicator(prices, sd - timedelta(days=22))
        prices = prices[sd:]

        orders_df = pd.DataFrame(index=prices.index, columns=[symbol])
        prices_iter = prices.iterrows()

        curr_holding = 0
        index, row = next(prices_iter)

        state = self.get_state_for_indicators(bb.ix[index][symbol], rsi.ix[index][symbol], macd.ix[index][symbol])
        action = self.q_learner.querysetstate(state)

        trade = self.calculate_trade(curr_holding,action)
        orders_df.ix[index][symbol] = self.get_action(action)
        curr_holding += trade

        for index, row in prices_iter:
            action = self.q_learner.querysetstate(state)
            sell_buy = self.get_action(action)
            orders_df.ix[index][symbol] = sell_buy
            curr_holding += trade
            state = self.get_state_for_indicators(bb.ix[index][symbol], rsi.ix[index][symbol],
                                                  macd.ix[index][symbol])
        return orders_df

 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    strl = StrategyLearner()
    strl.addEvidence()

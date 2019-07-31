"""
Student Name: Martin Mathew (replace with your name)
GT User ID: mmathew32 (replace with your User ID)
GT ID: 903241329 (replace with your GT ID)
"""
from math import sqrt

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return "mmathew32"

def get_order_data(order_file):
    df = pd.read_csv(order_file ,index_col="Date" ,usecols=['Date' ,'Symbol' ,'Order' ,'Shares'] ,parse_dates=True
                     ,na_values=['nan'])
    df.sort_index(axis=0 ,inplace=True)
    return df

def get_unique_symbols(df):
    return df.Symbol.unique().tolist()

def compute_portvals(orders_df,sym,sv,  commission=0.0, impact=0.):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    symbols = [sym]
    dates = pd.date_range(orders_df.first_valid_index(), orders_df.last_valid_index())
    price_df = get_price_df(dates, symbols)
    trade_df = make_trades(price_df, sym,orders_df,sv, commission, impact)
    portvals = calculate_port_val(trade_df, price_df, symbols+['Cash'])
    return portvals/portvals.ix[0]


def calculate_port_val(trade_df, prices_df, symbols):
    port_val = pd.DataFrame(index=trade_df.index, columns=["value"])
    for index, row in trade_df.iterrows():
        value = 0
        for sym in symbols:
            value += row[sym] * prices_df.ix[index][sym]
        port_val.ix[index]['value'] = value
    return port_val



def make_trades(prices_df, sym,order_df,sv, commision, impact):
    trades_df = prices_df.copy(deep=True)
    trades_df = trades_df.drop('SPY', axis=1)
    trades_df.ix[0:, 0:] = np.nan
    symbols = [sym]
    prev_holding = {sym: 0.0 for sym in symbols}
    prev_holding.update({'Cash': sv})
    for index, row in order_df.iterrows():
        current_stocks = 0.0
        current_cash = 0.0
        if index not in prices_df.index or prices_df.ix[index]['SPY'] is np.nan:
            continue
        if row[sym] == 0:
            current_stocks = prev_holding[sym]
            current_cash = prev_holding['Cash']
        elif row[sym] > 0:
            current_stocks = prev_holding[sym] + row[sym]
            current_cash = prev_holding['Cash'] - (
                        prices_df.ix[index][sym] * row[sym] + calculate_commision(
                    prices_df.ix[index][sym] * row[sym], commision, impact))
        else:
            current_stocks = prev_holding[sym] + row[sym]
            current_cash = prev_holding['Cash'] + prices_df.ix[index][sym] * abs(row[sym]) - calculate_commision(prices_df.ix[index][sym] * row[sym], commision, impact)

        trades_df.ix[index][sym] = current_stocks
        prev_holding[sym] = current_stocks
        trades_df.ix[index]['Cash'] = current_cash
        prev_holding['Cash'] = current_cash
    trades_df.fillna(method='ffill', inplace=True)
    trades_df.fillna(0, inplace=True)
    return trades_df


def calculate_commision(purchase_price, commision, impact):
    return commision + purchase_price * impact


def get_price_df(dates, symbols):
    price_df = get_data(symbols, dates)
    price_df = price_df[np.isfinite(price_df['SPY'])]
    price_df.fillna(method='ffill', inplace=True)
    price_df.fillna(method='bfill', inplace=True)
    price_df["Cash"] = 1.0
    return price_df


def get_sharpe_ratio(port_val):
    dr = port_val[1:] / port_val[:-1].values - 1
    return sqrt(252) * (dr.mean() / dr.std())


def get_cumulative_returns(port_val):
    return port_val.ix[-1] / port_val.ix[0] - 1


def get_std_dr(port_val):
    return (port_val[1:] / port_val[:-1].values - 1).std()


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    sharpe_ratio = get_sharpe_ratio(portvals)
    cum_ret = get_cumulative_returns(portvals)
    std_daily_ret = get_std_dr(portvals)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    # print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    # print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    # print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    # print
    # print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    # print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()

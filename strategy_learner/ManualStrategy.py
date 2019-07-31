

"""
Student Name: Martin Mathew (replace with your name)
GT User ID: mmathew32 (replace with your User ID)
GT ID: 903241329 (replace with your GT ID)
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from TheoreticallyOptimalStrategy import TheoriticalOptimalStrategy
from indicators import calculate_macd
from indicators import get_bollinger_band
from indicators import get_price_df
from indicators import get_rsi
from marketsimcode import compute_portvals


class ManualStrategy:

    def author(self):
        return "mmathew32"



    def calculate_trade(self,curr_holding, sell_buy):
        if curr_holding == 0 and sell_buy == 'B':
            return 1000
        elif curr_holding == 0 and sell_buy == 'S':
            return -1000
        elif curr_holding == 1000 and sell_buy == 'B':
            return 0
        elif curr_holding == 1000 and sell_buy == 'S':
            return -2000
        elif curr_holding == -1000 and sell_buy == 'B':
            return 2000
        elif curr_holding == -1000 and sell_buy == 'S':
            return 0

    def testPolicy(self,symbol , sd , ed , sv = 100000):
        bb = get_bollinger_band(sd,ed,[symbol],gen_fig=False)
        rsi = get_rsi(sd,ed,[symbol],gen_fig=False)
        macd = calculate_macd(sd,ed,[symbol],gen_fig=False)
        dates = pd.date_range(sd, ed)
        price_df = get_price_df(dates, [symbol])
        orders_df = pd.DataFrame(index=price_df.index, columns=[symbol])
        price_df_iter = price_df.iterrows()
        curr_holding = 0
        prev_index = None
        for index, row in price_df_iter:
            trade = self.trading_engine(bb,rsi,macd,prev_index,index,symbol,curr_holding)
            curr_holding += trade
            orders_df.ix[index][symbol] = trade
            prev_index = index
        return orders_df



    def trading_engine(self,bb,rsi,mac,prev_index,index,symbol,curr_holding):
        if(index in rsi.index and rsi.ix[index][symbol] is not np.nan and bb.ix[index][symbol] <= 0.0 and rsi.ix[index][symbol] < 50 and rsi.ix[index][symbol] > 20):
            return self.calculate_trade(curr_holding,"B")
        elif(index in rsi.index and rsi.ix[index][symbol] is not np.nan and bb.ix[index][symbol] is not  np.nan and bb.ix[index][symbol] > .95 and rsi.ix[index][symbol] > 50 and rsi.ix[index][symbol] < 75 ):
            return self.calculate_trade(curr_holding,"S")
        elif (index in rsi.index and rsi.ix[index][symbol] is not np.nan and prev_index is not None and mac.ix[index][symbol] > 0 and mac.ix[index][symbol] > mac.ix[prev_index][symbol] and rsi.ix[index][symbol] < 75):
            return self.calculate_trade(curr_holding,"B")
        elif (index in rsi.index and rsi.ix[index][symbol] is not np.nan and prev_index is not None and mac.ix[index][symbol] > 0 and mac.ix[index][symbol] < mac.ix[prev_index][symbol] and rsi.ix[index][symbol] > 75):
            return self.calculate_trade(curr_holding,"S")
        elif (index in rsi.index and rsi.ix[index][symbol] is not np.nan and prev_index is not None and mac.ix[index][symbol] < 0 and mac.ix[index][symbol] < mac.ix[prev_index][symbol] and rsi.ix[index][symbol] > 20):
            return self.calculate_trade(curr_holding,"S")
        elif (index in rsi.index and rsi.ix[index][symbol] is not np.nan and prev_index is not  None and mac.ix[index][symbol] < 0 and mac.ix[index][symbol] > mac.ix[prev_index][symbol] and rsi.ix[index][symbol] < 20):
            return self.calculate_trade(curr_holding,"B")
        else:
            return 0


def manual_in_sample():
    sd = '2008-01-01'
    ed = '2009-12-31'
    ms = ManualStrategy()
    manual_strategy_orders_df = ms.testPolicy('JPM', sd, ed, 100000)
    ts = TheoriticalOptimalStrategy()
    bench_mark_order = ts.make_bench_mark_order('JPM', sd, ed)
    manual_port_val = compute_portvals(manual_strategy_orders_df, 100000, 9.95, 0.005)
    bench_mark_port = compute_portvals(bench_mark_order, 100000, 9.95, 0.005)
    ax = manual_port_val.plot(title="Manual vs Benchmark", color="red", label="Theoritical Portfolio")
    bench_mark_port.plot(ax=ax, color="green", label="Benchmark Portfolio")
    manual_port_val.to_csv(r'ins.csv');
    manual_strategy_orders_df_iter = manual_strategy_orders_df.iterrows();
    print "********************In Sample*********************************"
    count = 0
    for index, row in manual_strategy_orders_df_iter:
        if (row['JPM'] > 0):
            count += 1
            ax.axvline(index, color='blue', linestyle='dashed')
        elif (row['JPM'] < 0):
            count += 1
            ax.axvline(index, color='black', linestyle='dashed')
    print "In Sample Count - {}".format(count)
    ax.set_xlabel("Date")
    ax.set_ylabel("Returns")
    print "Cululative Returns for benchmark - {}".format(bench_mark_port.iloc[-1] / bench_mark_port.iloc[0] - 1)
    print "Cululative Returns for portfolio - {}".format(manual_port_val.iloc[-1] / manual_port_val.iloc[0] - 1)
    print "SD for benchmark - {}".format(bench_mark_port.std())
    print "SD for portfolio - {}".format(manual_port_val.std())
    print "Mean for benchmark - {}".format(bench_mark_port.mean())
    print "Mean for portfolio - {}".format(manual_port_val.mean())
    ax.legend(["Manual Rule Based", "Benchmark"], loc="upper left")
    plt.savefig("manual_benchmark_in_sample.png")

def manual_out_sample():
    sd = '2010-01-01'
    ed = '2011-12-31'
    ms = ManualStrategy()
    manual_strategy_orders_df = ms.testPolicy('JPM', sd, ed, 100000)
    ts = TheoriticalOptimalStrategy()
    bench_mark_order = ts.make_bench_mark_order('JPM', sd, ed)
    manual_port_val = compute_portvals(manual_strategy_orders_df, 100000, 9.95, 0.005)
    bench_mark_port = compute_portvals(bench_mark_order, 100000, 9.95, 0.005)
    ax = manual_port_val.plot(title="Manual vs Benchmark", color="red", label="Theoritical Portfolio")
    bench_mark_port.plot(ax=ax, color="green", label="Benchmark Portfolio")
    manual_port_val.to_csv(r'ofs.csv')
    print "*****************************Out Of Sample********************************"
    count =0
    for index, row in manual_strategy_orders_df.iterrows():
        if (row['JPM'] is not 0):
            count += 1
    print "Out Of Sample Count - {}".format(count)
    print "Cululative Returns for benchmark - {}".format(bench_mark_port.iloc[-1] / bench_mark_port.iloc[0] - 1)
    print "Cululative Returns for portfolio - {}".format(manual_port_val.iloc[-1] / manual_port_val.iloc[0] - 1)
    print "SD for benchmark - {}".format(bench_mark_port.std())
    print "SD for portfolio - {}".format(manual_port_val.std())
    print "Mean for benchmark - {}".format(bench_mark_port.mean())
    print "Mean for portfolio - {}".format(manual_port_val.mean())
    ax.set_xlabel("Date")
    ax.set_ylabel("Returns")
    ax.legend(["Manual Rule Based", "Benchmark"], loc="upper left")
    plt.savefig("manual_benchmark_out_of_sample.png")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "in_sample":
        manual_in_sample()
    elif len(sys.argv) > 1 and sys.argv[1] == "out_sample":
        manual_out_sample()
    else:
        print "Usage : python ManualStrategy.py in_sample or python ManualStrategy.py out_sample"








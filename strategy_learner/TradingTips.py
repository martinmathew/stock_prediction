import pandas_datareader as pdr
import pandas as pd
from datetime import datetime, timedelta
from datetime import timedelta
import datetime as dt
import traceback
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals


def pull_historical_data(ticker_symbol,sd,ed):
    stoc_data = pdr.get_data_yahoo(symbols=ticker_symbol, start=sd, end=ed)
    stoc_data.to_csv("../data/{}.csv".format(ticker_symbol))
    print "Downloaded -{} data".format(ticker_symbol)


def get_cumulative_returns(port_val):
        return port_val.ix[-1] / port_val.ix[0] - 1

def read_stock_symbols(exchange):
    df_temp = pd.read_csv("../stocks/{}.csv".format(exchange), usecols=['Symbol'], na_values=['nan'])
    return df_temp

if __name__ == "__main__":
    today = datetime.now().date()
    start_in_sample_time = today - timedelta(days=910)
    end_in_sample_time = today - timedelta(days=181)

    start_out_sample_time = today - timedelta(days=180)
    end_out_sample_time = today
    df_sandp = read_stock_symbols("sandp")

    sandpiter = df_sandp.iterrows()
    end_day = datetime.now().date()
    start_day = end_day - timedelta(days=800)

    pull_historical_data('SPY', start_in_sample_time - timedelta(days=50), end_out_sample_time)

    investday = datetime.now().date()
    for row in sandpiter:
        try:
            sym = row[1]['Symbol']
            pull_historical_data(sym, start_in_sample_time - timedelta(days=50), end_out_sample_time)
            st = StrategyLearner(verbose=False,impact=0.0)
            print "Started Learning for - {}".format(sym)
            st.addEvidence(sym, sd=start_in_sample_time + timedelta(days=2), ed=end_in_sample_time, sv=1000)

            print "Started Testing on Out Sample - {}".format(sym)
            orders = st.testPolicy(sym,sd=start_out_sample_time,ed=end_out_sample_time)
            out_sample_port_val = compute_portvals(orders,sym,1000,0.0,0.0)
            cr = get_cumulative_returns(out_sample_port_val)

            print "Started Testing for trading - {}".format(sym)
            start_trade_day = dt.datetime(2019, 07, 22)
            trading_orders = st.testPolicy(sym, sd=start_trade_day, ed=end_out_sample_time)

            if cr[0] >0.0:
                print "*************************************************************************************"
                print "Cumulative in Out Sample for : {} : {}".format(sym, cr)
                for index, row in trading_orders.iterrows():
                    action = None
                    if row[sym] == 0:
                        action = "Hold"
                    elif row[sym] > 0:
                        action = "Buy"
                    elif row[sym] < 0:
                        action = "Sell"
                    print "{}:{}".format(index,action)
                print "**************************************************************************************"


        except:
            print"{} failed".format(row[1]['Symbol'])
            traceback.print_exc()

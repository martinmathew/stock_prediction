import pandas_datareader as pdr
import pandas as pd
from datetime import datetime, timedelta
from datetime import timedelta
import datetime as dt
import traceback
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals


def read_stock_symbols(exchange):
    df_temp = pd.read_csv("../stocks/{}.csv".format(exchange), usecols=['Symbol'], na_values=['nan'])
    return df_temp
"""
Student Name: Martin Mathew (replace with your name)
GT User ID: mmathew32 (replace with your User ID)
GT ID: 903241329 (replace with your GT ID)
"""
import pandas as pd


def author():
    return "mmathew32"


def get_bollinger_bounds(rm_df,r_std):
    return (rm_df + 2*r_std,rm_df - 2*r_std)

def get_bollinger_band(price_df):
    rm_df = pd.rolling_mean(price_df,window=20)
    r_std =pd.rolling_std(price_df,window=20)
    upper_bound,lower_bound = get_bollinger_bounds(rm_df,r_std)
    bbb = (price_df - lower_bound)/(upper_bound - lower_bound)
    return bbb



def get_rsi(price_df,lookback = 10):
    dr_df = price_df[1:] / price_df[:-1].values - 1
    dUp, dDown = dr_df.copy(), dr_df.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0
    RolUp = pd.rolling_mean(dUp, lookback)
    RolDown = pd.rolling_mean(dDown, lookback).abs()
    RS = RolUp / RolDown
    rsi = 100.0 - (100.0/(1.0 + RS))
    return rsi


def calculate_ema(price_df,loop_back):
    df = pd.DataFrame(index=price_df.index , data= price_df.ewm(span=loop_back, adjust=False).mean())
    return df



def calculate_macd(price_df):
    prices_ema_12_d = calculate_ema(price_df,12)
    prices_ema_26_d = calculate_ema(price_df,26)
    macd = prices_ema_12_d - prices_ema_26_d
    return macd







if __name__ == "__main__":
    sd ='2008-01-01'
    ed = '2009-12-31'
    bb = get_bollinger_band(sd,ed,['JPM'])
    rsi = get_rsi(sd,ed,['JPM'],10)
    macd = calculate_macd(sd,ed,['JPM'])


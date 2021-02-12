from os import close, write

from numpy.core.numeric import NaN
from numpy.core.numerictypes import _can_coerce_all
from numpy.lib.shape_base import column_stack
from numpy.ma.extras import flatten_inplace
from pandas.core.frame import DataFrame
#from settings import Settings
from config import parse_config,_parse_args
from starter import Starter, Buffer
from trader import create_trader
from signaler import Signal
import additional_libs.iqoptionapi.constants as api_constants
#import logging
import time
from datetime import datetime,timezone,timedelta
from pprint import pprint
from frame_dance import Robot

from patterns.curve_fit import CURVE_FIT
from patterns.base import Base
from patterns.bollinger_rsi import BOLLINGER_RSI
from patterns.two_min_cross import TWO_MIN_CROSS



import pandas as pd
import copy
from matplotlib import pyplot as plt
from numpy import arange
import numpy as np
from scipy.optimize import curve_fit
from stock_frame import StockFrame
from indicators import Indicators

args = _parse_args()
config = parse_config(args.config_path)

a = config.get_connection_username()
print(a)
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

be = Starter(config)
check, reason = be.create_connection()
print(check, reason)
be.api.change_balance('REAL')
print("REAL balance: ", be.api.get_balance())

print(be.change_balance_mode(config.get_balance_mode()))

print(be.api.check_connect())

all_markets = be.api.get_all_open_time()
current_open_markets = []
actives_not_open = []

for dirr in (['binary']):
    for symbol in all_markets[dirr]: 
        if all_markets[dirr][symbol]['open'] == True:
            current_open_markets.append(symbol)

#actives = current_open_markets
actives = ['EURUSD']
"""
traders = be.start_traders()

price_d = be.start_data_frame()

price_df = price_d.frame
df = price_df.frame
"""




#test = BOLLINGER_RSI('GBPUSD', price_d)

base = Base(be.api, actives=actives, candle_length=120)
   
candles_data = {}
no_of_candles = 999*5
exp = time.time()
candles_no = 999
n = 0
stockframe = None
while True:
    data = []
    for active in actives:
        candles_data[active] = base.candles(active, 120, 999, exp)

        for candle in candles_data[active]:
            mini_prices_dict={}
            mini_prices_dict['symbol'] = active
            mini_prices_dict['open'] = candle['open']
            mini_prices_dict['close'] = candle['close']
            mini_prices_dict['high'] = candle['max']
            mini_prices_dict['low'] = candle['min']
            mini_prices_dict['volume'] = candle['volume']
            mini_prices_dict['datetime'] = candle['from']
            data.append(mini_prices_dict)
    
    
    if stockframe == None:
        stockframe = StockFrame(data)
    else: stockframe.add_rows(data)

    first_bar_timestamp = data[0]['datetime']
    exp = first_bar_timestamp
    candles_no += 999
    n+=1
    print(n)

    if candles_no > no_of_candles: break
    
print(len(stockframe.frame))
indicator_client = Indicators(price_data_frame=stockframe)
# Add indicators
indicator_client.sma(30, 'sma30')
indicator_client.sma(14, 'sma14')
indicator_client.sma(6, 'sma6')
indicator_client.macd(12,26,'macd')
indicator_client.rsi(14,column_name='rsi14') 
indicator_client.change_in_price('price_diff')
indicator_client.add_crossover('macd_diff','macd','crossover_macd')
indicator_client.add_crossover('sma6','sma14','crossover_sma')
indicator_client.chopiness_index(14,'chopiness')
indicator_client.bollinger_bands(14)
indicator_client.stochastic_oscillator(14)
#indicator_client.volatility(20, 'v20')
    #indicator_client.volatility(75, 'v75')
    # Drop last row because of accuracy
stockframe.frame.drop(index=stockframe.frame.index[-1], inplace=True)
    
"""
with open("dataframeEURUSD1.txt",'w') as f:
    f.write(stockframe.frame.to_string())
print("printed")
"""
#
#stockframe.frame.sort_index(inplace=True)

#dataframe.reset_index(inplace=True)
#dataframe.drop(columns='symbol',inplace=True)
#dataframe.set_index('datetime', inplace=True)

#pprint(dataframe)
"""
sample = dataframe.sample(5)

daily_data = dataframe.resample('H').mean()
pprint(daily_data)

candles_pct_change = dataframe[['close']].pct_change()
candles_pct_change.fillna(0, inplace=True)
print(candles_pct_change)
print(candles_pct_change.describe())
candles_pct_change.hist(bins=50)


cum_candles_return = (1 + candles_pct_change).cumprod()

print(cum_candles_return)
cum_candles_return.plot()
plt.show()
"""

backtest_data = {}
for active in actives:
    trades = {}
    check_trade = {}
    dataframe = copy.deepcopy(stockframe.frame.loc[active])
    dataframe.drop(axis=0, index=dataframe.index[-1], inplace=True)
    dataframe.sort_index(inplace=True)
    dataframe.dropna(inplace=True)
    for i in range(len(dataframe)+1):
        if i == 0: continue
        sample = dataframe.iloc[:i]
        test = CURVE_FIT(active, sample)
        test1 = TWO_MIN_CROSS(active, sample)
        if test.call() or test1.call():
            trades_direction = 'call'
            
        elif test.put() or test1.call():
            trades_direction = 'put'
            
        else: trades_direction = None
        trades[i] = trades_direction
        if sample['price_diff'][-1] > 0: check = 'call'
        elif sample['price_diff'][-1] < 0: check = 'put'

        if i <= 1 or sample['price_diff'][-1] == 0 or trades[i-1] == None: continue
        if trades[i-1] == check:
            check_trade[i] = 1
        elif trades[i-1] != check:
            check_trade[i] = 0
        
    #print(check_trade)
    #print(dataframe.tail(1))
    count = 0
    count_l = 0
    for i in check_trade:
        if check_trade[i] == 1:
            print(i,':',check_trade[i],'...',dataframe.index[i])
            count += 1
    for i in check_trade:
        if check_trade[i] == 0:
            print(i,':',check_trade[i],'...',dataframe.index[i])
            count_l += 1
    print(active)
    print(count,'wins.',count_l,'losses.')



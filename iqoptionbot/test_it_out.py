from os import close, write

from numpy.core.numeric import NaN
from numpy.lib.shape_base import column_stack
from pandas.core.frame import DataFrame
#from settings import Settings
from config import parse_config,_parse_args
from starter import Starter, Buffer
from trader import create_trader
from signaler import Signal
import iqoptionapi.constants as api_constants
#import logging
import time
from datetime import datetime,timezone,timedelta
from pprint import pprint
from patterns.frame_dance import Robot

from patterns.test import TEST
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

#actives = be.check_open_markets()

traders = be.start_traders()

price_d = be.start_data_frame()

#price_df = price_d.frame
#df = price_df.frame

#with open("dataframe.txt",'a') as f:
    #f.write(df.to_string())

import pandas as pd
from matplotlib import pyplot
from numpy import arange
import numpy as np
from scipy.optimize import curve_fit,toms748

test = TEST('AUDUSD', price_d)

tail = test._frame_.tail(15)
print(tail)
#print(test.ma_future_cross())
"""
while test.ma_future_cross() != True:
    time.sleep(90)
    price_d.update_frame()
    print(test._frame_.tail())

print(test.ma_future_cross())
"""
"""
x=np.array([1,2,3,4,5])

y=tail.loc[:,'sma6'].values
z=tail.loc[:,'sma14'].values


o = np.polyfit(x,y,3)
f = np.poly1d(o)

m = np.polyfit(x,z,3)
n = np.poly1d(m)

x_new = np.linspace(x[0],x[-1],50)
y_new = f(x_new)
z_new = n(x_new)


g = f - n
x_bounds = np.linspace(x[-2],x[-1]+1,100)
idx = np.argwhere(np.diff(np.sign(g(x_bounds))))
#pyplot.plot(x[idx], f[idx], 'ro')
print(idx)
print(x_bounds[idx],f(x_bounds[idx]),g(x_bounds[idx]))

pyplot.figure()
pyplot.plot(x, y, 'o')
pyplot.plot(x, z, 'o')
pyplot.plot(x_new, z_new,'b--')
pyplot.plot(x_new, y_new,'g--')
pyplot.xlim(x[0]-1, x[-1]+2)
pyplot.show()
"""
"""
print(be.api.get_all_profit()['EURUSD']['turbo'])
"""

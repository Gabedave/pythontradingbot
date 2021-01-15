"""Module for IQ Option API TEST pattern."""

from time import daylight
from numpy.core.arrayprint import _none_or_positive_arg
from numpy.core.function_base import linspace
from numpy.core.numeric import cross
from pandas.core.frame import DataFrame
from patterns.base import Base
from patterns.indicators import Indicators
from patterns.frame_dance import Robot
import numpy as np

class CURVE_FIT():
    """Class for TEST1 pattern."""

    def __init__(self, active, stockframe):
        """
        :param api: The instance of
            :class:`IQ_Option <iqoptionapi.stable_api.IQ_Option>`.
        """
        #candle_length = 120
        #super(TEST, self).__init__(api, candle_length)
        self.name = "CURVE_FIT"
        self.stockframe = stockframe
        self.active = active
        self.duration = 2 #minutes
        
            
    @property
    def _frame_(self):
        self._frame = self.stockframe.frame.frame.loc[self.active]
        return self._frame

    def call(self):
        """Method to check call pattern."""
        rules = [self.macd_cross() == (True, 1),
        self.ma_cross() == (True,1),
        self.diffsma30() == (True,1),
        self.candles_colour() == 'green']
        
        rules_alt = [self.macd_cross() == (True, 1),
        self.ma_future_cross() == (True,1),
        self.diffsma30() == (True,1),
        self.candles_colour(1) == 'green',
        self.chopiness_test == True]

        if all(rules_alt):
            return True
        else: return False

    def put(self):
        """Method to check put pattern."""
        rules = [self.macd_cross() == (True, -1),
        self.ma_cross() == (True,-1),
        self.diffsma30() == (True,-1),
        self.candles_colour() == 'red']

        rules_alt = [self.macd_cross() == (True, -1),
        self.ma_future_cross() == (True,-1),
        self.diffsma30() == (True,-1),
        self.candles_colour(1) == 'red',
        self.chopiness_test == True]
        
        if all(rules) or all(rules_alt):
            return True
        else: return False
        
    def macd_cross(self):
        crossvalues = np.flip(self._frame_.loc[:,'crossover_macd'].values)
        candlespassed = 0
        for value in crossvalues:
            if (value != 0) and (candlespassed <= 3):
                return True, value
            elif candlespassed > 2:
                return False, None
            candlespassed += 1
        
    def ma_cross(self):
        crossover_sma = np.flip(self._frame_.loc[:,'crossover_sma'].values)
        if crossover_sma[0] == 1:
            return True, 1
        elif crossover_sma[0] == -1:
            return True, -1
        else:
            return False, None
        
    def diffsma30(self):
        rules = [self._frame_['sma6'].diff(1).iloc[-1] >= 0.00,#positive gradient
        np.sum(self._frame_['sma6'].iloc[-2:])/2 > self._frame_['sma30'].iloc[-1],#above sma30
        self._frame_['sma14'].diff(1).iloc[-1] >= 0.00,#positive gradient
        np.sum(self._frame_['sma14'].iloc[-2])/2 > self._frame_['sma30'].iloc[-1]]#above sma30

        rules1 = [self._frame_['sma6'].diff(1).iloc[-1] <= 0.00,#negative gradient
        np.sum(self._frame_['sma6'].iloc[-2:])/2 < self._frame_['sma30'].iloc[-1],#below sma30
        self._frame_['sma14'].diff(1).iloc[-1] <= 0.00,#negative gradient
        np.sum(self._frame_['sma14'].iloc[-2:])/2 < self._frame_['sma30'].iloc[-1]]#below sma30

        if all(rules):
            return True, 1
        elif all(rules1):
            return True, -1
        else:
            return False, None

    def candles_colour(self, number=2):
        mini_list = self._frame_['price_diff'].iloc[-number:].values
        if all(value >= 0 for value in mini_list):
            return 'green'
        if all(value <= 0 for value in mini_list):
            return 'red'

    def ma_future_cross(self):
        if self.macd_cross() == False:
            return False, None
        
        tail = self._frame_.tail()

        x=np.array([1,2,3,4,5])

        y=tail.loc[:,'sma6'].values
        z=tail.loc[:,'sma14'].values

        o = np.polyfit(x,y,3)
        f = np.poly1d(o) #sma6 curvefit

        m = np.polyfit(x,z,3)
        n = np.poly1d(m) #sma14 curvefit

        g = f - n
        x_bounds = np.linspace(x[-1],x[-1]+1,10)
        idx = np.diff(np.sign(g(x_bounds)))/2
        
        for value in idx:
            if value != 0:
                return True, value

        return False, None

    def chopiness_test(self):
        if self._frame_['chopiness'].iloc[-2:] <= 60:
            return True
        else: return False
    
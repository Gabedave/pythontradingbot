"""Module for IQ Option API TEST pattern."""

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
        #self._frame = self.stockframe.frame.frame.loc[self.active]
        self._frame = self.stockframe
        return self._frame

    def call(self):
        """Method to check call pattern."""
        rules = [
            self.macd_cross() == (True, 1),
            self.ma_future_cross() == (True,1),
            self.diffsma30() == (True,1),
            self.candles_colour(1) == 'green',
            self.bollinger_test(1) != (False, 1)
            #self.volatility_test() == True
            ]

        if all(rules):
            return True
        else: return False

    def put(self):
        """Method to check put pattern."""
        rules = [
            self.macd_cross() == (True, -1),
            self.ma_future_cross() == (True,-1),
            self.diffsma30() == (True,-1),
            self.candles_colour(1) == 'red',
            self.bollinger_test(1) != (False, -1)
            #self.volatility_test == True
            ]
        
        if all(rules):
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
        rules = [
            self._frame_['sma6'].diff(1).iloc[-1] >= 0.00,#positive gradient
            self._frame_['sma6'].iloc[-1] > self._frame_['sma30'].iloc[-1],#above sma30
            #self._frame_['sma14'].diff(1).iloc[-1] >= 0.00,#positive gradient
            self._frame_['sma14'].iloc[-1] > self._frame_['sma30'].iloc[-1]#above sma30
        ]

        rules1 = [
            self._frame_['sma6'].diff(1).iloc[-1] <= 0.00,#negative gradient
            self._frame_['sma6'].iloc[-1] < self._frame_['sma30'].iloc[-1],#below sma30
            #self._frame_['sma14'].diff(1).iloc[-1] <= 0.00,#negative gradient
            self._frame_['sma14'].iloc[-1] < self._frame_['sma30'].iloc[-1]#below sma30
        ]

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

        if len(tail) <= 4:
            return False, None
        
        y=tail['sma6'].values
        z=tail['sma14'].values
        
        x= np.arange(len(y)) +1
       
        o = np.polyfit(x,y,3)
        f = np.poly1d(o) #sma6 curvefit

        m = np.polyfit(x,z,3)
        n = np.poly1d(m) #sma14 curvefit

        g = f - n
        x_bounds = np.linspace(x[-1],x[-1]+1,20)
        idx = np.diff(np.sign(g(x_bounds)))/2
        
        for value in idx:
            if value != 0:
                return True, value

        return False, None

    def chopiness_test(self):
        if self._frame_['chopiness'].iloc[-2:] <= 60:
            return True
        else: return False

    def bollinger_test(self, number):
        a = self._frame_['close'].iloc[-number:].values
        b = self._frame_['band_upper'].iloc[-number:].values
        c = self._frame_['band_lower'].iloc[-number:].values
        
        if all(a[x] > b[x] for x in range(number)):
            return False, 1
        elif all(a[x] < c[x] for x in range(number)):
            return False, -1
        else: return True

    def volatility_test(self):
        a = self._frame_['v75'].iloc[-1].values
        if a > 0.016:
            return False

        else: return True
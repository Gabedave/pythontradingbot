"""Module for IQ Option API TEST pattern."""
import numpy as np

class TWO_MIN_CROSS():
    """Class for TEST pattern."""

    def __init__(self, active, stockframe):
        """
        :param api: The instance of
            :class:`IQ_Option <iqoptionapi.stable_api.IQ_Option>`.
        """
        #candle_length = 120
        #super(TEST, self).__init__(api, candle_length)
        self.name = "TWO_MINS_CROSS"
        self.stockframe = stockframe
        self.active = active
        self.duration = 2 #minutes
        
            
    @property
    def _frame_(self):
        self._frame = self.stockframe.frame.frame.loc[self.active]
        #self._frame = self.stockframe
        return self._frame

    def call(self):
        """Method to check call pattern."""
        rules = [self.macd_cross() == (True, 1),
        self.ma_cross() == (True,1),
        self.diffsma30() == (True,1),
        self.candles_colour() == 'green',
        self.rsi_test() <= 75,
        self.bollinger_test(1) != (False, 1)]

        if all(rules):
            return True
        else: return False

    def put(self):
        """Method to check put pattern."""
        rules = [self.macd_cross() == (True, -1),
        self.ma_cross() == (True,-1),
        self.diffsma30() == (True,-1),
        self.candles_colour() == 'red',
        self.rsi_test() >= 25,
        self.bollinger_test(1) != (False, -1)]
        
        if all(rules):
            return True
        else: return False
        
    def macd_cross(self):
        crossvalues = np.flip(self._frame_['crossover_macd'].values)
        candlespassed = 0
        for value in crossvalues:
            if (value != 0) and (candlespassed <= 2):
                return True, value
            elif candlespassed > 2:
                return False, None
            candlespassed += 1
        
    def ma_cross(self):
        crossover_sma = np.flip(self._frame_['crossover_sma'].values)
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
        np.sum(self._frame_['sma14'].iloc[-2:])/2 > self._frame_['sma30'].iloc[-1]]#above sma30

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

    def chopiness_test(self):
        if self._frame_['chopiness'].iloc[-2:] <= 60:
            return True
        else: return False

    def rsi_test(self):
        return self._frame_['rsi14'].iloc[-1]

    def bollinger_test(self, number):
        a = self._frame_['close'].iloc[-number:].values
        b = self._frame_['band_upper'].iloc[-number:].values
        c = self._frame_['band_lower'].iloc[-number:].values
        
        if all(a[x] > b[x] for x in range(number)):
            return False, 1
        elif all(a[x] < c[x] for x in range(number)):
            return False, -1
        else: return True
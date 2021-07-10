"""Module for IQ Option API TEST pattern."""
import numpy as np

class BOLLINGER_RSI():
    """Class for TEST pattern."""

    def __init__(self, active, stockframe):
        """
        :param api: The instance of
            :class:`IQ_Option <iqoptionapi.stable_api.IQ_Option>`.
        """
        #candle_length = 120
        #super(TEST, self).__init__(api, candle_length)
        self.name = "BOLLINGER_RSI"
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
        rules = [self.bollinger_test(1) == (True, 1),
        self.rsi_back() != (False, 1),
        all(i < 30 for i in self.rsi_test(1)),
        all(i < 20 for i in self.stoch_test(1)),
        self.candles_colour(1) == 'red'     
        ]
        rules_alt = [self.bollinger_test(1) == (True, 1),
        self.sma_gradient() >= 0,
        self.rsi_back() != (False, 1),
        self.candles_colour(1) == 'red']

        if all(rules_alt):
            return True
        else: return False

    def put(self):
        """Method to check put pattern."""
        rules = [self.bollinger_test(1) == (True, -1),
        self.rsi_back() != (False, -1),
        all(i > 70 for i in self.rsi_test(1)),
        all(i > 80 for i in self.stoch_test(1)),
        self.candles_colour(1) == 'green'
        ]
        rules_alt = [self.bollinger_test(1) == (True, -1),
        self.sma_gradient() <= 0,
        self.rsi_back() != (False, -1),
        self.candles_colour(1) == 'green']
        
        if all(rules_alt):
            return True
        else: return False
        
    def bollinger_test(self, number):
        a = self._frame_['close'].iloc[-number:].values
        b = self._frame_['band_upper'].iloc[-number:].values
        c = self._frame_['band_lower'].iloc[-number:].values
        
        if all(a[x] > b[x] for x in range(number)):
            return True, -1
        elif all(a[x] < c[x] for x in range(number)):
            return True, 1
        else: return False

    def rsi_test(self, number):
        return self._frame_['rsi14'].iloc[-number:]

    def stoch_test(self, number):
        return self._frame_['stoch_%K'].iloc[-number:]
    
    def candles_colour(self, number=2):
        mini_list = self._frame_['price_diff'].iloc[-number:].values
        if all(value >= 0 for value in mini_list):
            return 'green'
        if all(value <= 0 for value in mini_list):
            return 'red'

    def rsi_back(self):
        a = self.rsi_test(3).values
        b = self._frame_['rsi14'].iloc[-3:-1]
        if ((all(i >= 0 for i in np.diff(a))) \
            and all(i > 70 for i in a)) \
                or all(i > 70 for i in b):
            return False, -1
        elif ((all(i <= 0 for i in np.diff(a))) \
            and all(i < 30 for i in a)) \
                or all(i < 30 for i in b):
            return False, 1
            
        else: return True

    def back_test(self):
        if all(np.diff(self._frame_['rsi14'].iloc[-4:-1]) <= 0) and (self._frame_['rsi14'].iloc[-4] < 30) and\
            (self._frame_['price_diff'].iloc[-1] >= 0) and (self._frame_['sma30'].diff(15).iloc[-1] >= 0):
            return True, 1
        elif all(np.diff(self._frame_['rsi14'].iloc[-4:-1]) >= 0) and (self._frame_['rsi14'].iloc[-4] > 70) and\
            (self._frame_['price_diff'].iloc[-1] <= 0) and (self._frame_['sma30'].diff(15).iloc[-1] <= 0):
            return True, -1
        else: return False, None


    def sma_gradient(self):
        sma30_gradient = self._frame_['sma30'].diff(1).iloc[-1]
        
        band_middle_grad = self._frame_['sma14'].diff(1).iloc[-1]
        sma_gradient = (band_middle_grad + sma30_gradient)/2
        return sma_gradient
        


        """test_frame = self._frame_.iloc[:-1]
        if all(test_frame['close'].iloc[-3:] > test_frame['band_upper'].iloc[-3:]) and \
            (self._frame_['close'].iloc[-1] < self._frame_['band_upper'].iloc[-1]) and \
                (self._frame_['price_diff'].iloc[-1] <= 0):
            return True, -1
        elif all(test_frame['close'].iloc[-3:] < test_frame['band_lower'].iloc[-3:]) and \
            (self._frame_['close'].iloc[-1] > self._frame_['band_lower'].iloc[-1]) and \
                (self._frame_['price_diff'].iloc[-1] >= 0):
            return True, 1
        else: return False, None"""




            
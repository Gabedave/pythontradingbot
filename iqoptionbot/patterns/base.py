"""Module for IQ Option API base pattern."""
from datetime import datetime
from pprint import pprint
import time
import math
import copy
from datetime import timedelta


class Base(object):
    """Class for IQ Option API base pattern."""

    def __init__(self, api, actives, candle_length):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.

        Arguments:
        ----
        Api,
        Active,
        Candle length -> seconds,
        """
        self.api = api
        self.actives = actives
        self.candle_length = candle_length


    def candles(self, active, duration = None, no_of_candles = 60, endtime = None):
        """Method to get candles.
        
        Arguments:
        ----
        Active,
        Duration,
        No of candles,
        End time

        """
        if not duration:
            duration = self.candle_length
        if endtime:
            candles_data = self.api.get_candles(active, duration, no_of_candles, endtime)
        else: candles_data = self.api.get_candles(active, duration, no_of_candles, self.two_min_servertime.timestamp())

        #time.sleep(0.3)
        return candles_data

    def call(self):
        """Method to check call pattern."""
        pass

    def put(self):
        """Method to check put pattern."""
        pass

    def grab_prices_data(self):
        """Grabs the historical prices for all the postions in a portfolio.

        """
        print("Grabbing historical prices")
        self.two_min_servertime = None
        while not self.two_min_servertime:
            get_time = copy.deepcopy(self.api.get_server_timestamp_datetime())
            if (get_time.second == 0) and (get_time.minute) % 2 == 0:
                self.two_min_servertime = get_time - timedelta(microseconds=get_time.microsecond)
        
        candles_data = {}
        new_prices = []

        for active in self.actives:
            candles_data[active] = self.candles(active)
        
        for active in candles_data.keys():
            for candle in candles_data[active]:
                if candle['to'] > self.two_min_servertime.timestamp():
                    continue
                mini_prices_dict={}
                mini_prices_dict['symbol'] = active
                mini_prices_dict['open'] = candle['open']
                mini_prices_dict['close'] = candle['close']
                mini_prices_dict['high'] = candle['max']
                mini_prices_dict['low'] = candle['min']
                mini_prices_dict['volume'] = candle['volume']
                mini_prices_dict['datetime'] = candle['to']
                new_prices.append(mini_prices_dict)

        return new_prices

    def get_latest_bar(self):
        """Returns the latest bar for each symbol in the portfolio.

        Returns:
        ---
        {List[dict]} -- A simplified quote list.

        """        

        print("Waiting for next candle... few seconds")

        candles_data = {}
        latest_prices = []
        
        duration_last = 0
        while duration_last == 0:
            get_time = self.api.get_server_timestamp_datetime()
            if (get_time.second == 0) and (get_time.minute) % 2 == 0:
                duration_last = get_time - timedelta(microseconds=get_time.microsecond)
        
        time_diff = duration_last.timestamp() - self.two_min_servertime.timestamp()
        
        no_of_candles = int(time_diff / self.candle_length)
        if no_of_candles > 10: no_of_candles = 10

        self.two_min_servertime = duration_last
        
        for active in self.actives:
            candles_data[active] = self.candles(active, self.candle_length, no_of_candles=no_of_candles+1)
        
        for active in candles_data.keys():
            for candle in candles_data[active]:
                if candle['to'] > self.two_min_servertime.timestamp():
                    continue
                mini_prices_dict={}
                mini_prices_dict['symbol'] = active
                mini_prices_dict['open'] = candle['open']
                mini_prices_dict['close'] = candle['close']
                mini_prices_dict['high'] = candle['max']
                mini_prices_dict['low'] = candle['min']
                mini_prices_dict['volume'] = candle['volume']
                mini_prices_dict['datetime'] = candle['to']
                latest_prices.append(mini_prices_dict)
        
        return latest_prices

    
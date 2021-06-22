
from iqoptionbot.stock_frame import StockFrame
from iqoptionbot.patterns.base import Base
from iqoptionbot.indicators import Indicators

from datetime import datetime

class Robot():
    def __init__(self, api, actives) -> None:
        self.api = api
        self.actives = actives
        self.data = Base(self.api, self.actives, candle_length=120)
        
    
    def initiate_frame(self):
        
        prices_data = self.data.grab_prices_data()

        self.frame = StockFrame(prices_data)
        
        self.indicator_client = Indicators(price_data_frame=self.frame)

        # Add to the Stock Frame.

        return self.frame

    def update_frame(self):
        print("Updating stockframe")
        
        #if not self.frame.frame:self.initiate_frame()
        
        last_bar_datetime = self.frame.frame.tail(
        n=1
        ).index.get_level_values(1).values
        #pprint(self.frame)

        latest_bars = self.data.get_latest_bar()
        self.frame.add_rows(data=latest_bars)
        self.indicator_client.refresh()
        print('DataFrame updated',datetime.now())
        return self.frame

    def add_indicators(self):
        self.indicator_client.sma(30, 'sma30')
        self.indicator_client.sma(14, 'sma14')
        self.indicator_client.sma(6, 'sma6')
        self.indicator_client.macd(12,26,'macd')
        self.indicator_client.rsi(14,column_name='rsi14') 
        self.indicator_client.change_in_price('price_diff')
        self.indicator_client.add_crossover('macd_diff','macd','crossover_macd')
        self.indicator_client.add_crossover('sma6','sma14','crossover_sma')
        self.indicator_client.chopiness_index(14,'chopiness')
        self.indicator_client.bollinger_bands(14)
        self.indicator_client.stochastic_oscillator(14)
        self.indicator_client.volatility(10, 'v10')
        
        return self.frame

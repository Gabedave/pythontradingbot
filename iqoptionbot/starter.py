"""Module for IQ Option API starter."""

import os
import logging

from iqoptionapi.stable_api import IQ_Option
from config import parse_config, _parse_args
from signaler import create_signaler
from trader import create_trader
from frame_dance import Robot
from reporter import Report

import time


class Starter(object):
    """Calss for IQ Option API starter."""

    def __init__(self, config):
        """
        :param config: The instance of :class:`Settings
            <iqoptionpy.settings.settigns.Settings>`.
        """
        self.config = config
        self.api = IQ_Option(
            self.config.get_connection_username(),
            self.config.get_connection_password()
            )
        self.actives = config.get_trade_actives()

    def create_connection(self):
        """Method for create connection to IQ Option API."""
        logger = logging.getLogger(__name__)
        logger.info("Create connection.")

        try:
            check, reason = self.api.connect()
        except Exception as e:
            print('Error: ', e)

        if check:
            logger.info("Successfully connected.")
            if self.api.check_connect == False:
                print("Websocket did not respond")
        else:
            print("No Network")
        return check, reason

    def start_signalers(self, stockframe):
        """Method for start signalers."""
        logger = logging.getLogger(__name__)
        logger.info("Create signalers.")
        signalers = []
        patterns = self.config.get_trade_patterns()
        
        for active in self.actives:
            signaler = create_signaler(self.api, active, stockframe, self.balance)
            signaler.set_patterns(patterns)
            signaler.start()
            signalers.append(signaler)
        return signalers

    def start_traders(self):
        """Method for start traders."""
        logger = logging.getLogger(__name__)
        logger.info("Create traders.")
        traders = []
    
        for active in self.actives:
            trader = create_trader(self.api, active)
            trader.start()
            traders.append(trader)
        return traders
    
    def update_balance(self):
        self.balance = self.api.get_balance()

    def change_balance_mode(self, balance_mode):
        """Method to select balance mode."""
        self.api.change_balance(balance_mode)
        self.balance = self.api.get_balance()
        
        logger = logging.getLogger(__name__)
        logger.info("Changed balance to {}. Balance is {}".format(balance_mode,self.balance))
        return balance_mode, self.balance

    def start_data_frame(self):
        "Set up data frame"
        price_df = Robot(self.api, self.actives)
        price_df.initiate_frame()
        price_df.add_indicators()
        print("Stockframe initiated and indicators added")
        return price_df
    
    def check_open_markets(self):
        all_markets = self.api.get_all_open_time()
        current_open_markets = []
        actives_not_open = []

        for dirr in (['binary','turbo']):
            for symbol in all_markets[dirr]: 
                if all_markets[dirr][symbol]['open'] == True:
                    current_open_markets.append(symbol)

        for active in self.config.get_trade_actives():
            if active not in current_open_markets:
                actives_not_open.append(active)
        
        current_open_markets = list(set(self.config.get_trade_actives()) - set(actives_not_open))

        if actives_not_open:
            print("{} not open right now".format(actives_not_open))
            print("{} open".format(current_open_markets))
        else:
            print("All symbols open",self.actives)
        
        self.actives = current_open_markets
        if current_open_markets == []:
            print('Market closed for all actives')
            return None
        time.sleep(2)
        return self.actives

class Buffer:
    def __init__(self):
        self.buffer = 0
        self.signal = {}

    def activate(self, signal):
        self.buffer = time.time() + 100
        self.signal[signal.active] = self.buffer
    
    def check(self, signal):
        a = signal.active
        if a in self.signal:
            if time.time() > self.signal[a]:
                return True
            else: return False
        else: return True
        

def _prepare_logging():
    """Prepare logging for starter."""
    formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logs_folder = "logs"
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    starter_logger = logging.getLogger(__name__)
    starter_logger.setLevel(logging.INFO)

    starter_file_handler = logging.FileHandler(os.path.join(logs_folder, "starter.log"))
    starter_file_handler.setLevel(logging.DEBUG)
    starter_file_handler.setFormatter(formatter)

    starter_logger.addHandler(console_handler)
    starter_logger.addHandler(starter_file_handler)

    api_logger = logging.getLogger("iqoptionapi")

    api_file_handler = logging.FileHandler(os.path.join(logs_folder, "iqapi.log"))
    api_file_handler.setLevel(logging.DEBUG)
    api_file_handler.setFormatter(formatter)

    api_logger.addHandler(console_handler)
    api_logger.addHandler(api_file_handler)

    signaler_logger = logging.getLogger("signaler")
    signaler_logger.setLevel(logging.INFO)

    signaler_file_handler = logging.FileHandler(os.path.join(logs_folder, "signaler.log"))
    signaler_file_handler.setLevel(logging.DEBUG)
    signaler_file_handler.setFormatter(formatter)

    signaler_logger.addHandler(console_handler)
    signaler_logger.addHandler(signaler_file_handler)

    trader_logger = logging.getLogger("trader")
    trader_logger.setLevel(logging.INFO)

    trader_file_handler = logging.FileHandler(os.path.join(logs_folder, "trader.log"))
    trader_file_handler.setLevel(logging.DEBUG)
    trader_file_handler.setFormatter(formatter)

    trader_logger.addHandler(console_handler)
    trader_logger.addHandler(trader_file_handler)

    websocket_logger = logging.getLogger("websocket")

    websocket_file_handler = logging.FileHandler(os.path.join(logs_folder, "websocket.log"))
    websocket_file_handler.setLevel(logging.DEBUG)
    websocket_file_handler.setFormatter(formatter)

    websocket_logger.addHandler(console_handler)
    websocket_logger.addHandler(websocket_file_handler)

    balance_mode_logger = logging.getLogger("balance_mode")

    balance_mode_file_handler = logging.FileHandler(os.path.join(logs_folder, "balance_mode.log"))
    balance_mode_file_handler.setLevel(logging.DEBUG)
    balance_mode_file_handler.setFormatter(formatter)

    balance_mode_logger.addHandler(console_handler)
    balance_mode_logger.addHandler(balance_mode_file_handler)


def _create_starter(config):
    """Create IQ Option API starter.

    :param config: The instance of :class:`ConfigurationSettings
        <iqpy.configuration.settigns.ConfigurationSettings>`.

    :returns: Instance of :class:`Starter <iqpy.starter.Starter>`.
    """
    return Starter(config)


def start():
    """Main method for start."""
    args = _parse_args()
    config = parse_config(args.config_path)
    starter = _create_starter(config)
    buffer = Buffer()
    reporter = Report()

    _prepare_logging()
    starter.create_connection()
    starter.change_balance_mode(config.get_balance_mode())
    if not starter.check_open_markets():
        return "All Markets Closed"
    price_df = starter.start_data_frame()
    #stockframe = price_df.frame
    #print(stockframe.frame)

    signalers = starter.start_signalers(price_df)
    traders = starter.start_traders()
    
    t_end = time.time() + 10 * 60 * 60
    hr_mark = time.time() + 60*60
    result_count = 0
    

    while True:
        trade_ids = []
        for signaler in signalers:
            signal = signaler.get_signal()
            if signal and buffer.check(signal):
                
                print("signal received in {} direction".format(signal.direction))
                buffer.activate(signal)
                
                for trader in traders:
                    if signal.active == trader.active:
                        result, trade_id = trader.trade(signal)
                        if result: 
                            print("Trade for {} in direction {}:{}".format(signal.direction, signal.active, trade_id))
                            buffer.activate(signal)
                            trade_ids.append(trade_id)
                            result_count += 1
        reporter.report(trade_ids, os.path.join(os.path.dirname(__file__), "report.txt"))
        starter.update_balance()
        if time.time() >= hr_mark:
            starter.check_open_markets()
            hr_mark = time.time() + 60*60
        if time.time() >= t_end:
            print("Result count:",result_count)
            break
        price_df.update_frame()

if __name__ == "__main__":
    start()

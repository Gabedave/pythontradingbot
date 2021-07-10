"""Module for IQ Option API trader."""

import logging

class Trader(object):
    """Calls for IQ Option API trader."""

    def __init__(self, api, active):
        self.api = api
        self.active = active

    def start(self):
        """Method for start trader."""
        logger = logging.getLogger(__name__)

        #self.api.timesync.expiration_time = 1

        logger.info("Trader for active '%s' started.", self.active)

        logger.info("Trader for active '%s' wait for signal.", self.active)

    def trade(self, signal):
        """Method for trade."""
        logger = logging.getLogger(__name__)
        logger.info("Trader for active '%s' received signal '%s'.", self.active, signal.direction)

        result, trade_id = self.api.buy(
                signal.price,
                signal.active,  
                signal.direction,
                signal.duration
                )
        if result:
            logger.info("Trade successful for '%s'. Trade: '%s'. Id: '%s'", self.active, signal.direction, trade_id)
        else:
            logger.info("Trader for active '%s' not successful.\n'%s'", self.active, trade_id)

        return result, trade_id



def create_trader(api, active):
    """Method for create trader.

    :param api: The IQ Option API.
    :param active: The trader active.
    """
    logger = logging.getLogger(__name__)
    logger.info("Create trader for active '%s'.", active)
    return Trader(api, active)

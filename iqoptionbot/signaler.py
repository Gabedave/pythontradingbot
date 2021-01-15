"""Module for IQ Option API signaler."""
import logging
import patterns.constants as pattern_constants

class Signal(object):
    """Class for IQ Option API signal."""
    # pylint: disable=too-few-public-methods

    def __init__(self, price, active, direction, duration):
        self.direction = direction
        self.price = price
        self.active = active
        self.duration = duration


class Signaler(object):
    """Calss for IQ Option API signaler."""

    def __init__(self, api, active, stockframe, balance):
        self.api = api
        self.active = active
        self.patterns = []
        self.stockframe = stockframe
        self.balance = balance
        self.buy_amount = (5/100) * self.balance

    def start(self):
        """Method for start trading."""
        logger = logging.getLogger(__name__)

        #self.api.setactives([api_constants.ACTIVES[self.active]])
        logger.info("Signaler for active '%s' started.", self.active)

        for pattern in self.patterns:
            logger.info("Signaler for active '%s' wait for pattern '%s'.",
                        self.active, pattern.name)

    def set_patterns(self, patterns):
        """Method for set patterns.

        :param patterns: The list of patterns to wait signal.
        """
        for pattern in patterns:
            self.patterns.append(pattern_constants.PATTERNS[pattern](self.active, self.stockframe))

    def get_signal(self):
        """Get signal from patterns.

        :returns: The instance of :class:`Signal <signaler.signal.Signal>`.
        """
        logger = logging.getLogger(__name__)

        for pattern in self.patterns:
            if pattern.call():
                logger.info("Signaler for active '%s' received pattern '%s' in direction 'call'.",
                            self.active, pattern.name)
                self.set_buy_amount()
                if self.buy_amount < 1: self.buy_amount = 1
                return Signal(self.buy_amount, self.active, "call", pattern.duration)
            if pattern.put():
                logger.info("Signaler for active '%s' received pattern '%s' in direction 'put'.",
                            self.active, pattern.name)
                self.set_buy_amount()
                if self.buy_amount < 1: self.buy_amount = 1
                return Signal(self.buy_amount, self.active, "put", pattern.duration)

    def set_buy_amount(self):
        check, profit = self.api.check_last_win()
        if self.buy_amount <= 5*(5/100) * self.balance:
            if profit < 0:
                self.buy_amount = 2 * self.buy_amount
            if profit > 0:
                self.buy_amount = (5/100) * self.balance
        else: self.buy_amount = (5/100) * self.balance
        


def create_signaler(api, active, stockframe, balance):
    """Method for create signaler.

    :param api: The IQ Option API.
    :param active: The signaler active.
    """
    logger = logging.getLogger(__name__)
    logger.info("Create signaler for active '%s'.", active)
    return Signaler(api, active, stockframe, balance)

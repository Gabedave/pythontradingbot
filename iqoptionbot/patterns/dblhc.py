"""Module for IQ Option API DBLHC pattern."""

from iqoptionbot.patterns.base import Base


class DBLHC(Base):
    """Class for DBLHC pattern."""
    # pylint: disable=too-few-public-methods

    def __init__(self, api):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        super(DBLHC, self).__init__(api)
        self.name = "DBLHC"
        self.duration = 1

    def call(self):
        """Method to check call pattern."""
        if self.candles.first_candle.candle_low == self.candles.second_candle.candle_low:
            if self.candles.second_candle.candle_close > self.candles.first_candle.candle_low:
                return True

"""Module for IQ Option API trade pattern constants."""

from iqoptionbot.patterns.two_min_cross import TWO_MIN_CROSS
from iqoptionbot.patterns.dblhc import DBLHC
from iqoptionbot.patterns.dbhlc import DBHLC
from iqoptionbot.patterns.tbh import TBH
from iqoptionbot.patterns.tbl import TBL
from iqoptionbot.patterns.curve_fit import CURVE_FIT
from iqoptionbot.patterns.two_min_cross2 import TWO_MIN_CROSS2
from iqoptionbot.patterns.bollinger_rsi import BOLLINGER_RSI

PATTERNS = {
    "TWO_MIN_CROSS": TWO_MIN_CROSS,
    "TWO_MIN_CROSS2": TWO_MIN_CROSS2,
    "TBH": TBH,
    "TBL": TBL,
    "DBHLC": DBHLC,
    "DBLHC": DBLHC,
    "CURVE_FIT": CURVE_FIT,
    "BOLLINGER_RSI": BOLLINGER_RSI
}

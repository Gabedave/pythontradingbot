"""Module for IQ Option API trade pattern constants."""

from patterns.two_min_cross import TWO_MIN_CROSS
from patterns.dblhc import DBLHC
from patterns.dbhlc import DBHLC
from patterns.tbh import TBH
from patterns.tbl import TBL
from patterns.curve_fit import CURVE_FIT

PATTERNS = {
    "TWO_MIN_CROSS": TWO_MIN_CROSS,
    "TBH": TBH,
    "TBL": TBL,
    "DBHLC": DBHLC,
    "DBLHC": DBLHC,
    "CURVE_FIT": CURVE_FIT
}

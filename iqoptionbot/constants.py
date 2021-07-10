"""Module with constants for configuration."""

from decouple import config, Csv

# CONNECTION_SETTINGS_KEY = "connection_settings"
# CONNECTION_HOSTNAME_KEY = "hostname"
# CONNECTION_USERNAME_KEY = "username"
# CONNECTION_PASSWORD_KEY = "password"


# TRADE_SETTINGS_KEY = "trade_settings"
# TRADE_ACTIVES_KEY = "actives"
# TRADE_PATTERNS_KEY = "patterns"
# TRADE_BALANCE_MODE = "balance_mode


CONNECTION_SETTINGS_KEY = {
	'connection_hostname' : config('HOST', default='iqoption.com'),
	'connection_username' : config('USER', default=None),
	'connection_password' : config('KEY', default=None),
}

TRADE_SETTINGS_KEY = {
	'trade_actives' : config('ACTIVES', default=['EURUSD, EURUSD-OTC'], cast=Csv()),
	'trade_patterns' : config('PATTERNS', default=['TWO_MIN_CROSS','CURVE_FIT'], cast=Csv()),
	'trade_balance_mode' : config('BALANCE_MODE', default='PRACTICE'),
}

DEBUG = config('DEBUG', default=False, cast=bool)
from decouple import config

"connection_settings": {
    "hostname": "iqoption.com",
    "password": config('KEY'),
    "username": config('USER')
},
"trade_settings": {
    "actives": config('ACTIVES'), #list of Actives ['EURUSD','EURUSD-OTC']
    "patterns": config('PATTERNS'), #list of chosen patterns ['CURVE_FIT','TWO_MIN_CROSS']
    "balance_mode": config('BALANCE_MODE') #REAL or PRACTICE
}


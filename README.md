# Python Trading Bot(deployed as a Flask web app) using the IQ Option API

###Requirements installation

```
scipy
numpy
pandas
iqoptionapi
gunicorn
python-decouple
qtpylib
flask
```

###Basic usage:

Add configuration to environment variables
```
HOSTNAME=iqoption.com
USER={username}
KEY={password}


ACTIVES=USDCAD,EURGBP,EURUSD-OTC
PATTERNS=TWO_MIN_CROSS,CURVE_FIT
BALANCE_MODE=TWO_MIN_CROSS,CURVE_FIT
DEBUG=False
```

Start python trading bot:
```
In console: python starter.py
```

Logs can be found in 'logs' folder

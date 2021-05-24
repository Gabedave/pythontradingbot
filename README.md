# Python Trading Bot using the IQ Option API

###Requirements installation

```
pip install iqoptionapi
```

###Basic usage:

Create new configuration file:
```
python config.py -c config.json
```

Edit configuration file
```
{
    "connection_settings": {
        "hostname": "iqoption.com",
        "password": "password",
        "username": "username"
    },
    "trade_settings": {
        "actives": [
            "EURUSD-OTC",
            "EURUSD"
        ],
        "patterns": [
            "TEST",
            "TBH"
        ]
        "balance_mode": "PRACTICE"
    }
}
```

Start IQ Option bot:
```
python starter.py -c config.json
```

Logs can be found in 'logs' folder

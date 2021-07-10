# MODULE FOR TESTING FUNCTIONS OF THE APP

from iqoptionbot.config import _create_new_config
import iqoptionbot.constants as config_constants
import os

debug = config_constants.DEBUG

# LOAD CONFIGURATION TEST

def load_config_test(debug):
    try:
    	a = _create_new_config(debug)
    except Exception as e:
        print(e)
        return 'FAILED1'

    try:
        config: dict = a.config_data
    except Exception as e:
        print(e)
        return 'FAILED2'

    return 'LOAD CONFIG PASSED'

if __name__ == '__main__':
    print(load_config_test(debug))
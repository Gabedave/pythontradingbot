"""Module to work with execution configuration file."""
import logging
import argparse

from iqoptionbot.settings import Settings
from iqoptionbot.default import DefaultScenario

def create_config(debug):
    """
    Create configuration file.

    :param config_path: Path for new configuation file.
    """
    if debug == True:
        config = DefaultScenario()
        config.create_config()
        config = parse_config()
    else:
        config = parse_config()
    return config
        
    # config.settings.write_config(config_path)


def parse_config():
    """
    Obtain config from configuration file.

    :param config_path: Path of the configuation file.

    :returns: The config object.
    """
    config = Settings()
    config.load_config()
    return config

# def _parse_args():
#     """
#     Parse commandline arguments.

#     :returns: Instance of :class:`argparse.Namespace`.
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-c", "--config_path", dest="config_path", type=str, default='config/appenv.py',
#         help="Path to new configuration file.(default='config/appenv.py')"
#         )
#     return parser.parse_args()


def _create_new_config(debug = None):
    """Method for create new configuration file."""
    formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)
    # logger.addHandler(console_handler)

    settings_logger = logging.getLogger("settings")
    settings_logger.setLevel(logging.INFO)
    settings_logger.addHandler(console_handler)

    # args = _parse_args()

    return create_config(debug)


    # write function to take in variables from the front-end


if __name__ == "__main__":
    _create_new_config()

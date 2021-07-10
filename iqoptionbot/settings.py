"""Module for configuration settings."""
import json
import logging
import os

import iqoptionbot.constants as config_constants


class Settings(object):
    """Class for configuration settings."""
    # pylint: disable=too-many-public-methods

    def __init__(self):
        self.config_constants = config_constants
        self.__config_data = {}

    @property
    def config_data(self):
        """Property to get configuration data.

        :returns: The configuration data dictionary.
        """
        return self.__config_data

    @property
    def _connection_settings(self):
        """Property to get connection settings.

        :returns: The connection settings dictionary.
        """
        return self.config_constants.CONNECTION_SETTINGS_KEY

    def set_connection_hostname(self, connection_hostname):
        """Set connection hostname.

        :param connection_hostname: The connection hostname.
        """
        self._connection_settings['connection_hostname']= connection_hostname

    def get_connection_hostname(self):
        """Get connection hostname.

        :returns: The connection hostname.
        """
        return self._connection_settings['connection_hostname']

    def set_connection_username(self, connection_username):
        """Set connection username.

        :param connection_username: The connection username.
        """
        self._connection_settings['connection_username'] = connection_username

    def get_connection_username(self):
        """Get connection username.

        :returns: The connection username.
        """
        return self._connection_settings['connection_username']

    def set_connection_password(self, connection_password):
        """Set connection password.

        :param connection_password: The connection password.
        """
        self._connection_settings['connection_password'] = connection_password

    def get_connection_password(self):
        """Get connection password.

        :returns: The connection password.
        """
        return self._connection_settings['connection_password']

    @property
    def _trade_settings(self):
        """Property to get trade settings.

        :returns: The trade settings dictionary.
        """
        return self.config_constants.TRADE_SETTINGS_KEY

    def set_trade_actives(self, trade_actives):
        """Set trade actives.

        :param trade_actives: The list of trade actives.
        """
        self._trade_settings['trade_actives'] = trade_actives

    def get_trade_actives(self):
        """Get trade actives.

        :returns: The list of trade actives.
        """
        return self._trade_settings['trade_actives']

    def set_trade_patterns(self, trade_patterns):
        """Set trade patterns.

        :param trade_patterns: The list of trade patterns.
        """
        self._trade_settings['trade_patterns'] = trade_patterns

    def get_trade_patterns(self):
        """Get trade patterns.

        :returns: The list of trade patterns.
        """
        return self._trade_settings['trade_patterns']

    def set_balance_mode(self, trade_balance):
        """Set trade balance.

        :param trade_balance: the list of trade balance.
        """
        self._trade_settings['trade_balance_mode'] = trade_balance 

    def get_balance_mode(self):
        """Get trade patterns.

        :returns: balances mode.
        """
        return self._trade_settings['trade_balance_mode']


    def write_config(self, config):
        """Write configuration to Environment Variables

        :param config_path: The path to config file.
        """
        logger = logging.getLogger(__name__)
        logger.info("Create a new configuration")
        # STILL TO BE WRITTEN


    def load_config(self):
        """Load configuration from Environment Variables

        """
        logger = logging.getLogger(__name__)
        logger.info("Loading configuration from Environment Variables.")

        self.__config_data['connection_settings'] = self._connection_settings
        self.__config_data['trade_settings'] = self._trade_settings

        
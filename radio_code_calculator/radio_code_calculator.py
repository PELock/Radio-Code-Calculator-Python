#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface
#
# Generate radio unlocking codes for various radio players.
#
# Version      : v1.00
# Python       : Python v3
# Dependencies : requests (https://pypi.python.org/pypi/requests/)
# Author       : Bartosz Wójcik (support@pelock.com)
# Project      : https://www.pelock.com/products/radio-code-calculator
# Homepage     : https://www.pelock.com
#
###############################################################################

from enum import IntEnum
from typing import Optional, Dict, Union

# required external package - install with "pip install requests"
import requests
import re


class RadioErrors(IntEnum):
    """Errors returned by the Radio Code Calculator API interface"""

    # @var integer cannot connect to the Web API interface (network error)
    ERROR_CONNECTION: int = -1

    # @var integer successful request
    SUCCESS: int = 0

    # @var integer an error occurred while validating input data (invalid length, format etc.)
    INVALID_INPUT: int = 1

    # @var integer invalid Web API command (not supported)
    INVALID_COMMAND: int = 2

    # @var integer radio model is not supported by the calculator
    INVALID_RADIO_MODEL: int = 3

    # @var integer radio serial number is invalid (invalid format, not matching the expected regex pattern)
    INVALID_SERIAL_LENGTH: int = 4

    # @var integer radio serial number doesn't match the expected regular expression pattern
    INVALID_SERIAL_PATTERN: int = 5

    # @var integer radio serial number is not supported by the selected calculator
    INVALID_SERIAL_NOT_SUPPORTED: int = 6

    # @var integer extra data is invalid (invalid format, not matching the expected regex pattern)
    INVALID_EXTRA_LENGTH: int = 7

    # @var integer extra data doesn't match the expected regular expression pattern
    INVALID_EXTRA_PATTERN: int = 8

    # @var integer license key is invalid or expired
    INVALID_LICENSE: int = 100


class RadioModel(object):
    """A single radio model with its parameters"""
    name: str = ""

    serial_max_len: int = 0
    _serial_regex_patterns: dict[str, str] = {}

    extra_max_len: int = 0
    _extra_regex_patterns: Optional[dict[str, str]] = None

    @property
    def serial_regex_pattern(self):
        """Return the regex pattern only for the current programming language"""
        if "python" not in self._serial_regex_patterns:
            return ""
        return self._serial_regex_patterns["python"]

    @property
    def extra_regex_pattern(self):
        """Return the regex pattern only for the current programming language or None"""
        if self._extra_regex_patterns is None:
            return None
        if "python" not in self._extra_regex_patterns:
            return None

        return self._extra_regex_patterns["python"]

    def __init__(self,
                 name: str,
                 serial_max_len: int,
                 serial_regex_pattern: Union[str, dict[str, str]],
                 extra_max_len: int = 0,
                 extra_regex_pattern: Optional[Union[str, dict[str, str]]] = None):
        """Initialize RadioModel class with the radio model name, serial & extra fields max. length and regex pattern

        :param str name: Radio model name
        :param int serial_max_len: Max. serial length
        :param Union[str, dict[str, str]] serial_regex_pattern: Serial number single regex pattern or a dictionary
        :param int extra_max_len: Max. extra field length
        :param Optional[Union[str, dict[str, str]]] extra_regex_pattern: Extra field single regex pattern or a dictionary
        """
        self.name = name
        self.serial_max_len = serial_max_len

        # create an empty dict to prevent Python re-using previous dict from previous object (!)
        self._serial_regex_patterns = {}

        # store the regex pattern under the key for the current programming language (compatibility)
        if isinstance(serial_regex_pattern, str):
            self._serial_regex_patterns["python"] = serial_regex_pattern
        elif isinstance(serial_regex_pattern, dict):
            self._serial_regex_patterns = serial_regex_pattern

        # initialize extra field
        self.extra_max_len = extra_max_len
        self._extra_regex_pattern = None

        if extra_max_len:
            if isinstance(extra_regex_pattern, str):
                self._extra_regex_patterns["python"] = extra_regex_pattern
            elif isinstance(extra_regex_pattern, dict):
                self._extra_regex_patterns = extra_regex_pattern

    def validate(self, serial: str, extra: Optional[str] = None) -> int:
        """Validate radio serial number and extra data (if provided), check their lenghts and regex patterns

        :param str serial: Radio serial number
        :param Optional[str] extra: Extra data (optional)
        :return: one of the RadioErrors
        :rtype: int
        """

        if len(serial) != self.serial_max_len:
            return RadioErrors.INVALID_SERIAL_LENGTH
        if re.match(self.serial_regex_pattern, serial) is None:
            return RadioErrors.INVALID_SERIAL_PATTERN

        if extra is not None and len(extra) > 0:
            if len(extra) != self.extra_max_len:
                return RadioErrors.INVALID_EXTRA_LENGTH
            if re.match(self.extra_regex_pattern, extra) is None:
                return RadioErrors.INVALID_EXTRA_PATTERN

        return RadioErrors.SUCCESS


class RadioModels(object):
    """Supported radio models with the validation parameters (max. length & regex pattern)"""

    RENAULT_DACIA: RadioModel = RadioModel("renault-dacia", 4, r"^([A-Z]{1}[0-9]{3})$")
    CHRYSLER_PANASONIC_TM9: RadioModel = RadioModel("chrysler-panasonic-tm9", 4, r"^([0-9]{4})$")
    FORD_M_SERIES: RadioModel = RadioModel("ford-m-series", 6, r"^([0-9]{6})$")
    FORD_V_SERIES: RadioModel = RadioModel("ford-v-series", 6, r"^([0-9]{6})$")
    FORD_TRAVELPILOT: RadioModel = RadioModel("ford-travelpilot", 7, r"^([0-9]{7})$")
    FIAT_STILO_BRAVO_VISTEON: RadioModel = RadioModel("fiat-stilo-bravo-visteon", 6, r"^([a-zA-Z0-9]{6})$")
    TOYOTA_ERC: RadioModel = RadioModel("toyota-erc", 16, r"^([a-zA-Z0-9]{16})$")
    JEEP_CHEROKEE: RadioModel = RadioModel("jeep-cherokee", 14, r"^([a-zA-Z0-9]{10}[0-9]{4})$")


class RadioCodeCalculator(object):
    """Radio Code Calculator API module"""

    # 
    # @var string default Radio Code Calculator API WebApi endpoint
    # 
    API_URL: str = "https://www.wyznania.com/api/radio-code-calculator/v1"

    # 
    # @var string WebApi key for the service
    # 
    _apiKey: str = ""

    def __init__(self, api_key: str = ""):
        """Initialize Radio Code Calculator API class

        :param str api_key: Activation key for the service (it cannot be empty!)
        """

        self._apiKey = api_key

    def login(self) -> tuple[int, dict]:
        """Login to the service and get the information about the current license limits

        :return: A dictionary with the results or None on error
        :rtype: Optional[Dict]
        """

        # parameters
        params = {"command": "login"}

        result = self.post_request(params)
        return result["error"], result

    def calc(self, radio_model: Union[RadioModel, str], radio_serial_number: str, radio_extra_data: str = "") -> tuple[int, dict]:
        """List all the supported radio calculators and their parameters (name, max. len & regex pattern)

        :param Union[RadioModel, str] radio_model: Radio model either as a RadioModel class or a string
        :param str radio_serial_number: Radio serial number / pre code
        :param str radio_extra_data: Optional extra data (for example - a supplier code) to generate the radio code

        :return: An error code and an optional dictionary with the raw results
        :rtype: tuple[int, dict]:
        """

        # parameters
        params = {
            "command": "calc",
            "radio_model": radio_model if isinstance(radio_model, str) else radio_model.name,
            "serial": radio_serial_number,
            "extra": radio_extra_data,
        }

        result = self.post_request(params)
        return result["error"], result

    def info(self, radio_model: Union[RadioModel, str]) -> tuple[int, Optional[RadioModel]]:
        """Get the information about the given radio calculator and its parameters (name, max. len & regex pattern)

        :param Union[RadioModel, str] radio_model: Radio model either as a RadioModel class or a string
        :return: An error code and an optional RadioModel class
        :rtype: tuple[int, Optional[RadioModel]]:
        """

        # parameters
        params = {
            "command": "info",
            "radio_model": radio_model if isinstance(radio_model, str) else radio_model.name,
        }

        # send request
        result = self.post_request(params)

        if result["error"] != RadioErrors.SUCCESS:
            return result["error"], None

        model = RadioModel(params["radio_model"], result["serialMaxLen"], result["serialRegexPattern"],
                           result["extraMaxLen"], result["extraRegexPattern"])

        return result["error"], model

    def list(self) -> tuple[int, Optional[list[RadioModel]]]:
        """List all the supported radio calculators and their parameters (name, max. len & regex pattern)

        :return: A dictionary with the results or None on error
        :rtype: tuple[int, Optional[list[RadioModel]]]:
        """

        # parameters
        params = {"command": "list"}

        # send request
        result = self.post_request(params)

        if result["error"] != RadioErrors.SUCCESS:
            return result["error"], None

        radio_models: list[RadioModel] = []

        # enumerate supported radio models and build a list of RadioModel classes
        for radio_model_name in result["supportedRadioModels"]:

            radio_model = result["supportedRadioModels"][radio_model_name]

            model = RadioModel(radio_model_name, radio_model["serialMaxLen"],
                               radio_model["serialRegexPattern"], radio_model["extraMaxLen"],
                               radio_model["extraRegexPattern"])
            radio_models.append(model)

        return result["error"], radio_models

    def post_request(self, params_array: Dict[str, str]) -> Dict:
        """Send a POST request to the server

        :param Dict params_array: An array with the parameters
        :return: A dictionary with the results
        :rtype: Dict
        """

        # add activation key to the parameters array
        if self._apiKey:
            params_array["key"] = self._apiKey

        # default error -> only returned by the SDK
        default_error = {"error": RadioErrors.ERROR_CONNECTION}

        try:
            response = requests.post(self.API_URL, data=params_array)

            # no response at all or an invalid response code
            if not response or not response.ok:
                return default_error

            # decode to json array
            result = response.json()

            # return original JSON response code
            return result

        except Exception as ex:

            return default_error

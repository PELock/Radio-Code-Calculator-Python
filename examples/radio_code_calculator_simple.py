#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface usage example
#
# In this example, we will demonstrate how to generate a code for a specific
# type of car radio.
#
# Version        : v1.00
# Language       : Python
# Author         : Bartosz Wójcik
# Project        : https://www.pelock.com/products/radio-code-calculator
# Homepage       : https://www.pelock.com
#
###############################################################################

#
# include Radio Code Calculator API module
#
from radio_code_calculator import *

#
# create Radio Code Calculator API class instance (we are using our activation key)
#
myRadioCodeCalculator = RadioCodeCalculator("ABCD-ABCD-ABCD-ABCD")

#
# generate radio code (using Web API)
#
error, result = myRadioCodeCalculator.calc(RadioModels.FORD_M_SERIES, "123456")

if error == RadioErrors.SUCCESS:
    print(f'Radio code is {result["code"]}')
elif error == RadioErrors.INVALID_RADIO_MODEL:
    print("Invalid radio model (not supported)")
elif error == RadioErrors.INVALID_SERIAL_LENGTH:
    print(f'Invalid serial number length (expected {result["serialMaxLen"]} characters)')
elif error == RadioErrors.INVALID_SERIAL_PATTERN:
    print(f'Invalid serial number regular expression pattern (expected {result["serialRegexPattern"]["python"]} regex pattern)')
elif error == RadioErrors.INVALID_SERIAL_NOT_SUPPORTED:
    print("This serial number is not supported")
elif error == RadioErrors.INVALID_EXTRA_LENGTH:
    print(f'Invalid extra data length (expected {result["extraMaxLen"]} characters)')
elif error == RadioErrors.INVALID_EXTRA_PATTERN:
    print(f'Invalid extra data regular expression pattern (expected {result["extraRegexPattern"]["python"]} regex pattern)')
elif error == RadioErrors.INVALID_INPUT:
    print("Invalid input data")
elif error == RadioErrors.INVALID_COMMAND:
    print("Invalid command sent to the Web API interface")
elif error == RadioErrors.INVALID_LICENSE:
    print("Invalid license key")
elif error == RadioErrors.ERROR_CONNECTION:
    print("Something unexpected happen while trying to login to the service.")
else:
    print(f'Unknown error {error}')

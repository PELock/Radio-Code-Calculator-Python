#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface usage example
#
# In this example, we will demonstrate how to generate a code for a specific
# type of car radio. This example shows how to use an extended offline
# validation.
#
# Version        : v1.1.3
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
# generate a single radio unlocking code
#
serial: str = "123456"
extra: str = ""

#
# select a radio model
#
radioModel: RadioModel = RadioModels.FORD_M_SERIES

#
# display radio model information, you can use it to set limits in your controls e.g.
#
# textFieldRadioSerial.maxLength = radioModel.serial_max_len
# textFieldRadioSerial.regEx = radioModel.serial_regex_pattern
#
# (if allowed by your controls)
#
print(f'Radio model {radioModel.name} expects a serial number of {radioModel.serial_max_len}'
      f' length and {radioModel.serial_regex_pattern} regex pattern')

# additional information
if radioModel.extra_max_len > 0:
    print(f'Additionally an extra field is required with {radioModel.extra_max_len} and'
          f' and {radioModel.extra_regex_pattern} regex pattern')

#
# validate the serial number (offline) before sending the Web API request
#
error = radioModel.validate(serial, extra)

if error != RadioErrors.SUCCESS:

    if error == RadioErrors.INVALID_SERIAL_LENGTH:
        print(f'Invalid serial number length (expected {radioModel.serial_max_len} characters)')
    elif error == RadioErrors.INVALID_SERIAL_PATTERN:
        print(f'Invalid serial number regular expression pattern (expected {radioModel.serial_regex_pattern} regex pattern)')
    elif error == RadioErrors.INVALID_SERIAL_NOT_SUPPORTED:
        print("This serial number is not supported")
    elif error == RadioErrors.INVALID_EXTRA_LENGTH:
        print(f'Invalid extra data length (expected {radioModel.extra_max_len} characters)')
    elif error == RadioErrors.INVALID_EXTRA_PATTERN:
        print(f'Invalid extra data regular expression pattern (expected {radioModel.extra_regex_pattern} regex pattern)')
    exit(1)

#
# generate radio code (using Web API)
#
error, result = myRadioCodeCalculator.calc(radioModel, "123456")

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


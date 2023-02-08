#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface usage example
#
# In this example, we will demonstrate how to get information about the
# specific radio calculator and its parameters (max. length & regex pattern).
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
# query information about the radio model
#
error, radioModel = myRadioCodeCalculator.info("ford-m-series")

if error == RadioErrors.SUCCESS:

    print(f'Radio model name - {radioModel.name}')

    print(f'Max. length of the radio serial number - {radioModel.serial_max_len}')
    print(f'Regex pattern for the radio serial number - {radioModel.serial_regex_pattern}')

    # is extra field specified?
    if radioModel.extra_max_len > 0:
        print(f'Max. length of the radio extra data - {radioModel.extra_max_len}')
        print(f'Regex pattern for the radio extra data - {radioModel.extra_regex_pattern}')

    print()

elif error == RadioErrors.INVALID_LICENSE:
    print("Invalid license key!")
else:
    print(f'Something unexpected happen while trying to login to the service (error code {error}).')
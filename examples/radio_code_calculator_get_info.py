#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface usage example
#
# In this example, we will demonstrate how to get information about the
# specific radio calculator and its parameters (max. length & regex pattern).
#
# Version        : v1.1.5
# Language       : Python
# Author         : Bartosz Wójcik
# Project        : https://www.pelock.com/products/radio-code-calculator
# Homepage       : https://www.pelock.com
# Copyright      : (c) 2021-2024 PELock LLC
# License        : Apache-2.0
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
error, radio_model = myRadioCodeCalculator.info("ford-m-series")

if error == RadioErrors.SUCCESS:

    print(f'Radio model name - {radio_model.name}')

    print(f'Max. length of the radio serial number - {radio_model.serial_max_len}')
    print(f'Regex pattern for the radio serial number - {radio_model.serial_regex_pattern}')

    # is extra field specified?
    if radio_model.extra_max_len > 0:
        print(f'Max. length of the radio extra data - {radio_model.extra_max_len}')
        print(f'Regex pattern for the radio extra data - {radio_model.extra_regex_pattern}')

    print()

elif error == RadioErrors.INVALID_LICENSE:
    print("Invalid license key!")
else:
    print(f'Something unexpected happen while trying to login to the service (error code {error}).')

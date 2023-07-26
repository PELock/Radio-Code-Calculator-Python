#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface usage example
#
# In this example we will list all the available calculators and, their
# parameters like name, maximum length of the radio serial number and its
# regex pattern.
#
# Version        : v1.1.4
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
# get the list of the supported radio calculators and their parameters (max. length, regex pattern)
#
error, radio_models = myRadioCodeCalculator.list()

if error == RadioErrors.SUCCESS:

    print(f'Supported radio models {len(radio_models)}:\n')

    for radio_model in radio_models:

        print(f'Radio model name - {radio_model.name}')

        print(f'Max. length of the radio serial number - {radio_model.serial_max_len}')
        print(f'Regex pattern for the radio serial number - {radio_model.serial_regex_pattern}')

        # is extra field specified?
        if radio_model.extra_max_len > 0:
            print(f'Max. length of the radio extra data - {radio_model.extra_max_len}')
            print(f'Regex pattern for the radio extra data - {radio_model.extra_regex_pattern}')

        print()

elif error == RadioErrors.INVALID_LICENSE:
    print("Invalid activation key!")
else:
    print(f'Something unexpected happen while trying to login to the service (error code {error}).')

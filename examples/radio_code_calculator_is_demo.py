#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface usage example
#
# In this example we will verify our activation key status.
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
# login to the service
#
error, result = myRadioCodeCalculator.login()

#
# result[] array holds the information about the license
#
# result["license"]["activationStatus"] - True if license is active, False on invalid/expired keys
# result["license"]["userName"] - user name/company name of the license owner
# result["license"]["type"] - license type (0 - Personal License, 1 - Company License)
# result["license"]["expirationDate"] - license expiration date (in YYYY-MM-DD format)
#
if error == RadioErrors.SUCCESS:
    print(f'License activation status - {"True" if result["license"]["activationStatus"] else "False"}')
    print(f'License owner - {result["license"]["userName"]}')
    print(f'License type - {"Personal" if result["license"]["type"] == 0 else "Company"}')
    print(f'Expiration date - {result["license"]["expirationDate"]}')

elif error == RadioErrors.INVALID_LICENSE:
    print("Invalid license key!")
else:
    print(f'Something unexpected happen while trying to login to the service (error code {error}).')

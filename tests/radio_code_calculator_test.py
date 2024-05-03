#!/usr/bin/env python

###############################################################################
#
# Radio Code Calculator API - WebApi interface unit test
#
# Validate Radio Code Calculator Web API responses
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

import unittest

#
# make sure to provide valid activation key in order to run the tests
#
VALID_ACTIVATION_KEY = "ABCD-ABCD-ABCD-ABCD"


class TestRadioCodeCalculator(unittest.TestCase):

    #
    # global instance of RadioCodeCalculator
    #
    myRadioCodeCalculator: RadioCodeCalculator

    #
    # enter valid license key here to make sure the tests will run
    #
    apiKey: str = VALID_ACTIVATION_KEY

    def __init__(self, *args, **kwargs):

        super(TestRadioCodeCalculator, self).__init__(*args, **kwargs)

        #
        # create Radio Code Calculator API class instance (we are using our activation key)
        #
        self.myRadioCodeCalculator = RadioCodeCalculator(self.apiKey)

    def test_login(self):

        # login to the service
        error, result = self.myRadioCodeCalculator.login()

        self.assertIsNotNone(result)
        self.assertIn('error', result)
        self.assertEqual(result['error'], RadioErrors.SUCCESS)
        self.assertIn("license", result)
        self.assertIn("userName", result["license"])
        self.assertIn("type", result["license"])
        self.assertIn("expirationDate", result["license"])

    def test_login_invalid(self):

        # provide invalid license key
        radioCodeApi = RadioCodeCalculator("AAAA-BBBB-CCCC-DDDD")

        # login to the service
        error, result = radioCodeApi.login()

        self.assertIsNotNone(result)
        self.assertIn('error', result)
        self.assertEqual(result['error'], RadioErrors.INVALID_LICENSE)

    def test_invalid_radio_model(self):

        # login to the service
        error, result = self.myRadioCodeCalculator.calc("INVALID RADIO MODEL", "1234")

        self.assertIsNotNone(result)
        self.assertIn('error', result)
        self.assertEqual(result['error'], RadioErrors.INVALID_RADIO_MODEL)

    def test_radio_command(self):

        # send invalid command to the service
        params = {"command": "INVALID COMMAND"}

        result = self.myRadioCodeCalculator.post_request(params)

        self.assertIsNotNone(result)
        self.assertIn('error', result)
        self.assertEqual(result['error'], RadioErrors.INVALID_COMMAND)

    def test_radio_codes(self):

        # valid pair of radio codes to test the calculator
        codes = {
            RadioModels.RENAULT_DACIA: ["Z999", "0060"],
            RadioModels.CHRYSLER_PANASONIC_TM9: ["1234", "8865"],
            RadioModels.FORD_M_SERIES: ["123456", "2487"],
            RadioModels.FORD_V_SERIES: ["123456", "3067"],
            RadioModels.FORD_TRAVELPILOT: ["1234567", "3982"],
            RadioModels.FIAT_STILO_BRAVO_VISTEON: ["999999", "4968"],
            RadioModels.FIAT_DAIICHI: ["6461", "8354"],
            RadioModels.FIAT_VP: ["2063", "1341"],
            RadioModels.TOYOTA_ERC: ["10211376ab8e0d25", "A6905892"],
            RadioModels.JEEP_CHEROKEE: ["TQ1AA1500E2884", "1315"],
            RadioModels.NISSAN_GLOVE_BOX: ["D4CDDC568498", "55B7AB0BAB6F"],
            RadioModels.ECLIPSE_ESN: ["7D4046", "15E0ED"],
            RadioModels.JAGUAR_ALPINE: ["99999", "6125"],
        }

        for model in codes:

            # offline validate input first
            self.assertEqual(model.validate(codes[model][0]), RadioErrors.SUCCESS)

            # validate radio code for the given serial number
            error, result = self.myRadioCodeCalculator.calc(model, codes[model][0])

            self.assertIsNotNone(result)
            self.assertIn('error', result)
            self.assertEqual(error, RadioErrors.SUCCESS, model.name)
            self.assertEqual(result['error'], RadioErrors.SUCCESS)
            self.assertEqual(result['code'], codes[model][1], model.name)

    def test_radio_code_len(self):

        # invalid radio serial length
        error, result = self.myRadioCodeCalculator.calc(RadioModels.FORD_M_SERIES, "1")

        self.assertIsNotNone(result)
        self.assertIn('error', result)
        self.assertEqual(error, RadioErrors.INVALID_SERIAL_LENGTH)
        self.assertEqual(result['error'], RadioErrors.INVALID_SERIAL_LENGTH)

    def test_radio_code_pattern(self):

        # calculate the code with invalid regex pattern
        error, result = self.myRadioCodeCalculator.calc(RadioModels.FORD_M_SERIES, "12345A")

        self.assertIsNotNone(result)
        self.assertIn('error', result)
        self.assertEqual(error, RadioErrors.INVALID_SERIAL_PATTERN)
        self.assertEqual(result['error'], RadioErrors.INVALID_SERIAL_PATTERN)


if __name__ == '__main__':
    unittest.main()

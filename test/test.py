#!/usr/bin/env python

import sys, os
import unittest
import random
from client import Payment

TEST_API_KEY='6202349b8068b349b6e0b389be2a65cc36847c75'
TEST_BASE_URL='https://staging.beyonic.com/api/'
TEST_PAYMENT_ID = 23
TEST_PAYMENT_UPDATE_ID = 3718
TEST_NEW_STATUS = 'new'
TEST_STATUS = 200

class TestBeyonicApi(unittest.TestCase):
    def setUp(self):
        self.payment = Payment(TEST_API_KEY, TEST_BASE_URL)

    def test001_create_payments(self):
        """
        Get all the payments
        """
        data = {'phonenumber': '+256773712831', 'amount': 100, 'currency': 'UGX', 'description': 'sample description'}
        res, status = self.payment.create(data)

        if res:
            if type(res) is list:
                res = res[len(res)-1]
            else: #printing response
                print res
        else:
            res = []

        status = res.get('state', None)

        self.assertAlmostEqual(TEST_NEW_STATUS, status)

    def test002_create_payments(self):
        """
        Get all the payments
        """
        data = {'phonenumber': '+256773712831', 'amount': 100, 'currency': 'UGX', 'description': 'sample description'}
        res, status = self.payment.create(data)

        if res:
            if type(res) is list:
                res = res[len(res)-1]
            else: #printing response
                print res
        else:
            res = []

        status = res.get('state', None)

        self.assertAlmostEqual(TEST_NEW_STATUS, status)

    def test003_get_payments(self):
        """
        Get all the payments
        """
        res,status = self.payment.list()
        if res:
            if type(res) is list:
                res = res[0]
        else:
            res = []

        self.assertAlmostEqual(TEST_PAYMENT_ID, res.get('id', None))


if __name__ == "__main__":
    unittest.main()
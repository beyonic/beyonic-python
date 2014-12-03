#!/usr/bin/env python

import sys, os
import unittest
import random
import beyonic

TEST_API_KEY = '6202349b8068b349b6e0b389be2a65cc36847c75'
TEST_BASE_URL = 'https://staging.beyonic.com/api/'

'''
' Beyonic Test Cases
'''
class BeyonicTestCase(unittest.TestCase):
    def setUp(self):
        super(BeyonicTestCase, self).setUp()

        beyonic.api_key = TEST_API_KEY
        beyonic.api_endpoint_base = TEST_BASE_URL

        #During testing, let's turn off secure mode
        beyonic.verify_ssl_certs = False


    def tearDown(self):
        super(BeyonicTestCase, self).tearDown()



'''
' Payment Test Cases
'''

'''
class PaymentTestCase(BeyonicTestCase):

    def test001_list(self):
        #Test all payments related methods
        payments = beyonic.Payment.list()
        print payments

        self.assertAlmostEqual(1, 10)

'''

'''
' WebHooks Test Cases
'''

'''
class WebHooksTestCase(BeyonicTestCase):
    def test001_list(self):
        #Test all payments related methods

        webhooks = beyonic.Webhook.list()
        print webhooks

        self.assertAlmostEqual(1, 1)

'''

'''
class UrlFetchClientTest(BeyonicTestCase):
    #getting webhooks using urlfetch client lib
    def test001_webhookslist(self):
        from beyonic.api_client import UrlFetchClient
        webhooks = beyonic.Webhook.list(client=UrlFetchClient())
'''

class RequestsClientTest(BeyonicTestCase):
    #getting webhooks using requests client lib
    '''
    def test001_webhookslist(self):
        from beyonic.api_client import RequestsClient
        webhooks = beyonic.Webhook.list(client=RequestsClient(verify_ssl_certs=False))
        print webhooks

        #TODO
    '''
    def test002_webhookscreate(self):
        from beyonic.api_client import RequestsClient
        webhook = beyonic.Webhook.create(client=RequestsClient(verify_ssl_certs=False), event="payment.status.changed", target="https://my.callback.url/")
        print webhook

if __name__ == "__main__":
    unittest.main()
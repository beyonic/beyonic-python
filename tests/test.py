#!/usr/bin/env python

import sys, os
import unittest
import random
import beyonic
from beyonic.api_client import RequestsClient, UrlFetchClient

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

        # During testing, let's turn off secure mode
        beyonic.verify_ssl_certs = False


    def tearDown(self):
        super(BeyonicTestCase, self).tearDown()


'''
RequestClient test cases.
'''


class RequestsClientTest(BeyonicTestCase):
    # getting webhooks using requests client lib
    def test001_webhooks_list(self):
        webhooks = beyonic.Webhook.list(client=RequestsClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(webhooks))

    # creating new webhook
    def test002_webhooks_create(self):
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=RequestsClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

    #getting single webhook
    def test003_webhook_create_get(self):
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=RequestsClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(target, refreshed_webhook.target)
        self.assertEqual(event, refreshed_webhook.event)

    #updating webhook using update method
    def test004_webhook_update_get(self):
        web_id = 10
        new_target = "https://mysite.com/callbacks/payment/updated"
        webhook = beyonic.Webhook.update(id=web_id, client=RequestsClient(verify_ssl_certs=False), target=new_target)
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)

    #updating webhook using save
    def test005_webhook_save_get(self):
        web_id = 10
        new_target = "https://mysite.com/callbacks/payment/saved"
        webhook = beyonic.Webhook.get(id=web_id, client=RequestsClient(verify_ssl_certs=False))
        webhook.target = new_target
        webhook.save()
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)

    #deleting webhook
    def test005_webhook_create_delete(self):
        #creating new hook
        target = "https://mysite.com/callbacks/payment/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=RequestsClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        #deleting the hook
        is_deleted = beyonic.Webhook.delete(webhook.id)
        self.assertTrue(is_deleted)


    # getting payment using requests client lib
    def test006_payments_list(self):
        payments = beyonic.Payment.list(client=RequestsClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(payments))

    #creating new payment
    def test007_payment_create(self):
        phonenumber = "+256773712831"
        amount = 2000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'

        payment = beyonic.Payment.create(client=RequestsClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url)

        self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(description, payment.description)

    #creating & getting single payment
    def test008_payment_create_get(self):
        phonenumber = "+256773712831"
        amount = 4000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'

        payment = beyonic.Payment.create(client=RequestsClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url)

        self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(description, payment.description)

        refreshed_payment = beyonic.Payment.get(id=payment.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertIn(phonenumber, refreshed_payment.phone_nos)
        self.assertEqual(description, refreshed_payment.description)


'''
UrlFetchClient test cases.
'''
class UrlFetchClientTest(BeyonicTestCase):
    # getting webhooks using urlfetch client lib

    def test001_webhooks_list(self):
        webhooks = beyonic.Webhook.list(client=UrlFetchClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(webhooks))

    # creating new webhook
    def test002_webhooks_create(self):
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=UrlFetchClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

    #getting single webhook
    def test003_webhook_create_get(self):
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=UrlFetchClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertEqual(target, refreshed_webhook.target)
        self.assertEqual(event, refreshed_webhook.event)

    #updating webhook using update method
    def test004_webhook_update_get(self):
        web_id = 10
        new_target = "https://mysite.com/callbacks/payment/updated"
        webhook = beyonic.Webhook.update(id=web_id, client=UrlFetchClient(verify_ssl_certs=False), target=new_target)

        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)

    #updating webhook using save
    def test005_webhook_save_get(self):
        web_id = 10
        new_target = "https://mysite.com/callbacks/payment/saved"
        webhook = beyonic.Webhook.get(id=web_id, client=UrlFetchClient(verify_ssl_certs=False))
        webhook.target = new_target
        webhook.save()
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)

    #deleting webhook
    def test005_webhook_create_delete(self):
        #creating new hook
        target = "https://mysite.com/callbacks/payment/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=UrlFetchClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        #deleting the hook
        is_deleted = beyonic.Webhook.delete(webhook.id)
        self.assertTrue(is_deleted)

    # getting payment using urlfetch client lib
    def test006_payments_list(self):
        payments = beyonic.Payment.list(client=UrlFetchClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(payments))

    #creating new payment
    def test007_payment_create(self):
        phonenumber = "+256773712831"
        amount = 2000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'

        payment = beyonic.Payment.create(client=UrlFetchClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url)

        self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(description, payment.description)

    #creating & getting single payment
    def test008_payment_create_get(self):
        phonenumber = "+256773712831"
        amount = 4000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'

        payment = beyonic.Payment.create(client=UrlFetchClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url)

        self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(description, payment.description)

        refreshed_payment = beyonic.Payment.get(id=payment.id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertIn(phonenumber, refreshed_payment.phone_nos)
        self.assertEqual(description, refreshed_payment.description)


if __name__ == "__main__":
    unittest.main()
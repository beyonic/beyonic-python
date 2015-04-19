#!/usr/bin/env python

import sys, os
import unittest
import random
import beyonic
from beyonic.api_client import RequestsClient, UrlFetchClient

TEST_API_KEY = '312726d359422c52d986e6a67f713cdf42eb9f96'
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

    # getting single webhook
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
        web_id = 49
        new_target = "https://mysite.com/callbacks/payment/updated"
        webhook = beyonic.Webhook.update(id=web_id, client=RequestsClient(verify_ssl_certs=False), target=new_target)
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)

    #updating webhook using save
    def test005_webhook_save_get(self):
        web_id = 49
        new_target = "https://mysite.com/callbacks/payment/saved"
        webhook = beyonic.Webhook.get(id=web_id, client=RequestsClient(verify_ssl_certs=False))
        webhook.target = new_target
        webhook.save()
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)

    #deleting webhook
    def test006_webhook_create_delete(self):
        #creating new hook
        target = "https://mysite.com/callbacks/payment/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=RequestsClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        #deleting the hook
        is_deleted = beyonic.Webhook.delete(webhook.id)
        self.assertTrue(is_deleted)

    def test007_webhooks_list_save(self):
        webhooks = beyonic.Webhook.list(client=RequestsClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(webhooks))

        #updating individual object
        webhook = webhooks[0]
        new_target = "https://mysite.com/callbacks/payment/saved/1"
        webhook.target = new_target
        webhook.save()
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)


    # getting payment using requests client lib
    def test008_payments_list(self):
        payments = beyonic.Payment.list(client=RequestsClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(payments))

    #creating new payment
    def test009_payment_create(self):
        phonenumber = "+256773712831"
        amount = 2000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'
        payment_type = 'money'

        payment = beyonic.Payment.create(client=RequestsClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url, payment_type=payment_type)

        #self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(payment_type, payment.payment_type)
        self.assertEqual(description, payment.description)

    #creating & getting single payment
    def test010_payment_create_get(self):
        phonenumber = "+256773712831"
        amount = 4000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'
        payment_type = 'money'

        payment = beyonic.Payment.create(client=RequestsClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url, payment_type=payment_type)

        #self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(payment_type, payment.payment_type)
        self.assertIn(description, payment.description)

        refreshed_payment = beyonic.Payment.get(id=payment.id, client=RequestsClient(verify_ssl_certs=False))
        #self.assertIn(phonenumber, refreshed_payment.phone_nos)
        self.assertIn(payment_type, refreshed_payment.payment_type)
        self.assertEqual(description, refreshed_payment.description)


    def test011_collection_list(self):
        collections = beyonic.Collection.list(client=RequestsClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(collections))


    def test012_collection_get(self):
        collection_id = 1
        collection = beyonic.Collection.get(id=collection_id, client=RequestsClient(verify_ssl_certs=False))
        self.assertEqual(collection.id, collection.id)


    def test013_collection_search(self):
        collections = beyonic.Collection.list(client=RequestsClient(verify_ssl_certs=False), phonenumber='+254727843600', organization='5')
        self.assertLessEqual(1, len(collections))

    def test014_collection_claim(self):
        collections = beyonic.Collection.list(client=RequestsClient(verify_ssl_certs=False), claim=True, phonenumber='+254727843600', remote_transaction_id=None, amount='200')
        self.assertLessEqual(1, len(collections))

    def test015_create_collectionrequst(self):
        phonenumber = "+256773712831"
        amount = '1200'
        currency='UGX'
        collection_request = beyonic.CollectionRequest.create(client=RequestsClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency)

        self.assertIn(phonenumber, collection_request.phonenumber)
        self.assertEqual(currency, collection_request.currency)

        refreshed_collection_request = beyonic.CollectionRequest.get(id=collection_request.id, client=RequestsClient(verify_ssl_certs=False))
        self.assertIn(phonenumber, refreshed_collection_request.phonenumber)
        self.assertEqual(currency, refreshed_collection_request.currency)

    def test016_list_collection_requests(self):
        collections_requests = beyonic.CollectionRequest.list(client=RequestsClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(collections_requests))


###
#Url Fetch test cases
###

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
    def test006_webhook_create_delete(self):
        #creating new hook
        target = "https://mysite.com/callbacks/payment/"
        event = "payment.status.changed"
        webhook = beyonic.Webhook.create(client=UrlFetchClient(verify_ssl_certs=False), event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        #deleting the hook
        is_deleted = beyonic.Webhook.delete(webhook.id)
        self.assertTrue(is_deleted)

    def test007_webhooks_list_save(self):
        webhooks = beyonic.Webhook.list(client=UrlFetchClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(webhooks))

        #updating individual object
        webhook = webhooks[0]
        new_target = "https://mysite.com/callbacks/payment/saved/1"
        webhook.target = new_target
        webhook.save()
        refreshed_webhook = beyonic.Webhook.get(id=webhook.id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertEqual(new_target, refreshed_webhook.target)


    # getting payment using urlfetch client lib
    def test008_payments_list(self):
        payments = beyonic.Payment.list(client=UrlFetchClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(payments))

    #creating new payment
    def test009_payment_create(self):
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
    def test010_payment_create_get(self):
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

    def test011_collection_list(self):
        collections = beyonic.Collection.list(client=UrlFetchClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(collections))


    def test012_collection_get(self):
        collection_id = 1
        collection = beyonic.Collection.get(id=collection_id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertEqual(collection.id, collection.id)


    def test013_collection_search(self):
        collections = beyonic.Collection.list(client=UrlFetchClient(verify_ssl_certs=False), phonenumber='+254727843600', organization='5')
        self.assertLessEqual(1, len(collections))

    def test014_collection_claim(self):
        collections = beyonic.Collection.list(client=UrlFetchClient(verify_ssl_certs=False), claim=True, phonenumber='+254727843600', remote_transaction_id=None, amount='200')
        self.assertLessEqual(1, len(collections))

    def test015_create_collectionrequst(self):
        phonenumber = "+256773712831"
        amount = '1200'
        currency='UGX'
        collection_request = beyonic.CollectionRequest.create(client=UrlFetchClient(verify_ssl_certs=False), phonenumber=phonenumber,
                                         amount=amount, currency=currency)

        self.assertIn(phonenumber, collection_request.phonenumber)
        self.assertEqual(currency, collection_request.currency)

        refreshed_collection_request = beyonic.CollectionRequest.get(id=collection_request.id, client=UrlFetchClient(verify_ssl_certs=False))
        self.assertIn(phonenumber, refreshed_collection_request.phonenumber)
        self.assertEqual(currency, refreshed_collection_request.currency)

    def test016_list_collection_requests(self):
        collections_requests = beyonic.CollectionRequest.list(client=UrlFetchClient(verify_ssl_certs=False))
        self.assertLessEqual(1, len(collections_requests))


if __name__ == "__main__":
    unittest.main()
import unittest
import random
import shutil
from time import sleep
import os
import logging

from nose import SkipTest
from config import BeyonicTestCase, tape
from beyonic.api_client import RequestsClient

'''
# Uncomment below lines if you want to debug vcrpy


logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from vcrpy
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.DEBUG)
'''


"""Test Cases"""

'''
Request Client
'''
class RequestsClientTest(BeyonicTestCase):
    client = RequestsClient(verify_ssl_certs=False)
    # getting webhooks using requests client lib


    @tape.use_cassette('webhooks_list.json')
    def test001_webhooks_list(self):
        webhooks = self.beyonic.Webhook.list(client=self.client)
        self.assertLessEqual(1, len(webhooks.results))



    # creating new webhook
    @tape.use_cassette('webhooks_create.json')
    def test002_webhooks_create(self):
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = self.beyonic.Webhook.create(client=self.client, event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)


    # getting single webhook
    @tape.use_cassette('webhooks_create.json')
    def test003_webhook_create_get(self):
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = self.beyonic.Webhook.create(client=self.client, event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        with tape.use_cassette('webhooks_get.json'):
            refreshed_webhook = self.beyonic.Webhook.get(id=webhook.id, client=self.client)

        #hack
        str(refreshed_webhook)
        self.assertEqual(target, refreshed_webhook.target)
        self.assertEqual(event, refreshed_webhook.event)


    #updating webhook
    @tape.use_cassette('webhooks_update.json')
    def test004_webhook_update_get(self):
        web_id = 52
        new_target = "https://mysite.com/callbacks/payment/updated"
        webhook = self.beyonic.Webhook.update(id=web_id, client=self.client, target=new_target)
        refreshed_webhook = self.beyonic.Webhook.get(id=webhook.id, client=self.client)
        self.assertEqual(new_target, refreshed_webhook.target)



    #updating webhook using save
    @tape.use_cassette('webhooks_save_get.json')
    def test005_webhook_save_get(self):
        web_id = 52
        new_target = "https://mysite.com/callbacks/payment/saved"
        webhook = self.beyonic.Webhook.get(id=web_id, client=self.client)

        webhook.target = new_target
        webhook.save()

        refreshed_webhook = self.beyonic.Webhook.get(id=webhook.id, client=self.client)
        self.assertEqual(new_target, refreshed_webhook.target)



    #deleting webhook
    @tape.use_cassette('webhooks_delete.json')
    def test006_webhook_create_delete(self):
        #creating new hook
        target = "https://my.callback.url/"
        event = "payment.status.changed"
        webhook = self.beyonic.Webhook.create(client=self.client, event=event, target=target)

        self.assertEqual(target, webhook.target)
        self.assertEqual(event, webhook.event)

        #deleting the hook
        is_deleted = self.beyonic.Webhook.delete(webhook.id)
        self.assertTrue(is_deleted)



    #list save
    @tape.use_cassette('webhooks_list_update.json')
    def test007_webhooks_list_save(self):
        webhooks = self.beyonic.Webhook.list(client=self.client)
        self.assertLessEqual(1, len(webhooks))

        #updating individual object
        webhook = webhooks.results[0]
        new_target = "https://mysite.com/callbacks/payment/saved/1"
        webhook.target = new_target
        webhook.save()
        refreshed_webhook = self.beyonic.Webhook.get(id=webhook.id, client=self.client)
        self.assertEqual(new_target, refreshed_webhook.target)



    # getting payment using requests client lib
    @tape.use_cassette('payments_list.json')
    def test008_payments_list(self):
        payments = self.beyonic.Payment.list(client=self.client)
        self.assertLessEqual(1, len(payments.results))



    #creating new payment
    @tape.use_cassette('payments_create.json')
    def test009_payment_create(self):
        phonenumber = "+256773712831"
        amount = 2000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'
        payment_type = 'money'

        payment = self.beyonic.Payment.create(client=self.client, phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url, payment_type=payment_type)

        #self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(payment_type, payment.payment_type)
        self.assertEqual(description, payment.description)



    #creating & getting single payment
    @tape.use_cassette('payments_create_get.json')
    def test010_payment_create_get(self):
        phonenumber = "+256773712831"
        amount = 4000
        currency = 'UGX'
        description = 'Sample description'
        callback_url = 'https://google.com'
        payment_type = 'money'

        payment = self.beyonic.Payment.create(client=self.client, phonenumber=phonenumber,
                                         amount=amount, currency=currency, description=description,
                                         callback_url=callback_url, payment_type=payment_type)

        #self.assertIn(phonenumber, payment.phone_nos)
        self.assertEqual(payment_type, payment.payment_type)
        self.assertIn(description, payment.description)

        refreshed_payment = self.beyonic.Payment.get(id=payment.id, client=self.client)
        #self.assertIn(phonenumber, refreshed_payment.phone_nos)
        self.assertIn(payment_type, refreshed_payment.payment_type)
        self.assertEqual(description, refreshed_payment.description)



    #collection list
    @tape.use_cassette('collections_list.json')
    def test011_collection_list(self):
        collections = self.beyonic.Collection.list(client=self.client)
        self.assertLessEqual(1, len(collections.results))



    #collection get
    @tape.use_cassette('collections_get.json')
    def test012_collection_get(self):
        with tape.use_cassette('collections_list.json'):
            collections = self.beyonic.Collection.list(client=self.client)
            collection_id = collections.results[0]['id']
        collection = self.beyonic.Collection.get(id=collection_id, client=self.client)
        self.assertEqual(collection.id, collection.id)



    @tape.use_cassette('collections_search.json')
    def test013_collection_search(self):
        collections = self.beyonic.Collection.list(client=self.client, phonenumber='+2547227272723', remote_transaction_id='12132')
        self.assertLessEqual(1, len(collections))


    @tape.use_cassette('collections_claim.json')
    def test014_collection_claim(self):
        collections = self.beyonic.Collection.list(client=self.client, claim=True, phonenumber='+254727843600', remote_transaction_id=None, amount='200')
        self.assertLessEqual(1, len(collections))



    #creating collection request
    @tape.use_cassette('collection_request_create.json')
    def test015_create_collectionrequst(self):
        phonenumber = "+256772781923"
        amount = '3000'
        currency='UGX'
        collection_request = self.beyonic.CollectionRequest.create(client=self.client, phonenumber=phonenumber,
                                         amount=amount, currency=currency)

        self.assertIn(phonenumber, collection_request.phonenumber)
        self.assertEqual(currency, collection_request.currency)

        refreshed_collection_request = self.beyonic.CollectionRequest.get(id=collection_request.id, client=self.client)
        self.assertIn(phonenumber, refreshed_collection_request.phonenumber)
        self.assertEqual(currency, refreshed_collection_request.currency)


    #collection request list
    @tape.use_cassette('collection_request_list.json')
    def test016_list_collection_requests(self):
        collections_requests = self.beyonic.CollectionRequest.list(client=self.client)
        self.assertLessEqual(1, len(collections_requests.results))

    # getting accounts lit using the client
    @tape.use_cassette('accounts_list.json')
    def test017_accounts_list(self):
        payments = self.beyonic.Account.list(client=self.client)
        self.assertLessEqual(1, len(payments.results))



if __name__ == '__main__':
    unittest.main()

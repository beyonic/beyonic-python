import os
import vcr
import unittest
import beyonic
from beyonic.api_client import RequestsClient, UrlFetchClient

TEST_API_KEY = '312726d359422c52d986e6a67f713cdf42eb9f96'
TEST_BASE_URL = 'https://staging.beyonic.com/api/'
TEST_API_VERSION = 'v1'

tape = vcr.VCR(
    cassette_library_dir='vcr_cassettes',
    filter_headers=['Authorization'],
    serializer='json',
    record_mode='once',
    match_on = ['uri', 'method'],
)

class BeyonicTestCase(unittest.TestCase):
    def setUp(self):
        super(BeyonicTestCase, self).setUp()
        self.beyonic = beyonic
        self.beyonic.api_version = TEST_API_VERSION
        self.beyonic.api_key = TEST_API_KEY
        self.beyonic.api_endpoint_base = TEST_BASE_URL

        # During testing, let's turn off secure mode
        self.beyonic.verify_ssl_certs = False


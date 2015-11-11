import os
import vcr
import unittest
import beyonic
from beyonic.api_client import RequestsClient, UrlFetchClient

# Test on staging
TEST_API_KEY = '312726d359422c52d986e6a67f713cdf42eb9f96'
TEST_BASE_URL = 'https://staging.beyonic.com/api/'
TEST_API_VERSION = None

# Test on localhost
TEST_API_KEY = 'ceb16a7353367f09328d2f324eaeb89744f9bd22'
TEST_BASE_URL = 'http://localhost:8000/api/'
TEST_API_VERSION = 'v2'  # Test the various versions to ensure we're still as BC as possible

tape = vcr.VCR(
    cassette_library_dir='vcr_cassettes',
    filter_headers=['Authorization'],
    serializer='json',
    record_mode='once',
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


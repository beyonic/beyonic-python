from _bsddb import api
import os
from datetime import datetime
import time
import socket
import urllib

try:
    import json
except ImportError:
    import simplejson as json

API_VERSION = 'api/v1/'
DEFAULT_BASE_URL = 'https://app.beyonic.com/'

'''
Custom exception class
'''


class BeyonicError(Exception):
    pass


is_request = False
is_urlfetch = False
'''
let's try to import requests if its available
'''
try:
    import requests
    is_request = True
except ImportError:
    '''
    requests not available so let's try to import urlfetch
    '''
    try:
        import urlfetch
        is_urlfetch = True
    except ImportError:
        '''
        url fetch is also not available to let's throw an error
        '''
        raise BeyonicError(
            'Either of requests or urlfetch is not installed. Please install either of them using requirements.txt')


class Base(object):
    def __init__(self, api_key=None, base_url=None):
        if not base_url:
            base_url = os.path.join(DEFAULT_BASE_URL, API_VERSION)

        if not api_key:
            try:
                api_key = os.environ['BEYONIC_ACCESS_KEY']
            except KeyError:
                raise BeyonicError('BEYONIC_ACCESS_KEY not set.')

        self.base_url = base_url
        self.api_key = api_key

    def _build_request(self, url, method, data=None):
        """
        `method` must be one of 'GET', 'POST', 'PUT', or 'DELETE'.
        """
        if not url:
            raise BeyonicError('A url must be specified.')

        if data:
            body = json.dumps(data)
        else:
            body = ''

        headers = {
            'Authorization': 'Token ' + self.api_key,
            'Content-Type': 'application/json',
        }

        if is_request:
            if method == 'GET':
                r = requests.get(url, headers=headers, verify=False)
            elif method == 'POST':
                r = requests.post(url, headers=headers, data=body, verify=False)
            elif method == 'PUT':
                r = requests.put(url, headers=headers, data=body, verify=False)
            elif method == 'DELETE':
                r = requests.delete(url, headers=headers, verify=False)

            try:
                r_data = r.json()
                r_status = r.status_code
            except:  # most likely a JSONDecodeError
                raise BeyonicError(r)

        elif is_urlfetch:
            if method == 'GET':
                r = urlfetch.fetch(url, headers=headers)
            elif method == 'POST':
                r = urlfetch.post(url, headers=headers, data=body)

            try:
                r_data = json.loads(r.content)
                r_status = r.status
            except:
                raise BeyonicError(r)
        else:
            raise BeyonicError(
                'Either of requests or urlfetch is not installed. Please install either of them using requirements.txt')


        return r_data, r_status


'''
Payment api wrapper class
'''


class Payment(Base):
    method_path = 'payments'

    '''
    api_key: The Beyonic api key. Beyonic uses Token Based Authentication, and requires an API key for authentication.
    base_url: the api url including version e.g. https://staging.beyonic.com/api/
    '''

    def __init__(self, api_key=None, base_url=None):
        super(Payment, self).__init__(api_key, base_url)

    def list(self):
        """
        This will return list of payments.
        """
        method_type = 'GET'
        url = os.path.join(self.base_url, self.method_path)
        return self._build_request(url, method_type)

    def create(self, data):
        """
        This will create a new payment object and return as dict obj
        """
        method_type = 'POST'
        url = os.path.join(self.base_url, self.method_path)

        if not data:
             raise BeyonicError('Please provide request data')

        return self._build_request(url, method_type, data)

    def update(self, id, data):
        """
        This will create a new payment object and return as dict obj
        """
        method_type = 'PUT'
        url = os.path.join(self.base_url, self.method_path)

        if not data:
             raise BeyonicError('Please provide request data')

        return self._build_request(url, method_type, data)



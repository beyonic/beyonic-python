'''
# This return the api client. It should first check if requests is installed, if its installed then returns RequestsClient,
# if requests is not installed then check for urlfetch lib, if its installed then return its client UrlfetchClient
# if both of them not installed then throws the exception
'''

import textwrap
from beyonic.errors import BeyonicError, ResponseError
from beyonic.resources import GenericObject
import os
import beyonic
# let's try to import requests if its available
try:
    import requests
except ImportError:
    requests = None


# let's try to import urlfetch
try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None


class BaseClient(object):
    def __init__(self, verify_ssl_certs=True):
        self._verify_ssl_certs = verify_ssl_certs


class RequestsClient(BaseClient):
    name = 'requests'

    def request(self, method, url, headers, params=None):
        if not requests:
            raise BeyonicError('requests is not installed. Please install/setup it first using pip. e.g. pip install requests>=1.0')

        kwargs = {}

        if self._verify_ssl_certs:
            kwargs['verify'] = True
        else:
            kwargs['verify'] = False

        try:
            try:
                if method.upper() == 'GET':
                    result = requests.request(method,
                                          url,
                                          headers=headers,
                                          params=params,
                                          timeout=80,
                                          **kwargs)
                else:
                    result = requests.request(method,
                                          url,
                                          headers=headers,
                                          data=params,
                                          timeout=80,
                                          **kwargs)
            except TypeError, e:
                raise TypeError(
                    'Please upgrade your request library. The '
                    'underlying error was: %s' % (e,))

            content = result.content
            status_code = result.status_code
        except Exception, e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self._handle_request_error(e)
        return content, status_code

    def _handle_request_error(self, e):
        msg = ("Unexpected error communicating with Beyonic API.")
        err = "A %s was raised" % (type(e).__name__,)
        if str(e):
            err += " with error message %s" % (str(e),)
        else:
            err += " with no error message"
        msg = textwrap.fill(msg) + "\n\n(error: %s)" % (err,)
        raise BeyonicError(msg)


class UrlFetchClient(BaseClient):
    name = 'urlfetch'

    def request(self, method, url, headers, params=None):
        if not urlfetch:
            raise BeyonicError('urlfetch is not installed. Please install/setup it first.')
        try:
            result = urlfetch.fetch(
                url=url,
                method=method,
                headers=headers,

                validate_certificate=self._verify_ssl_certs,
                deadline=55,
                payload=params
            )
        except urlfetch.Error, e:
            self._handle_request_error(e, url)

        return result.content, result.status_code

    def _handle_request_error(self, e, url):
        if isinstance(e, urlfetch.InvalidURLError):
            msg = ("Unexpected error communicating with Beyonic API.")
        elif isinstance(e, urlfetch.DownloadError):
            msg = "There was a problem retrieving data from Beyonic."
        elif isinstance(e, urlfetch.ResponseTooLargeError):
            msg = ("Unexpected error communicating with Beyonic API.")
        else:
            msg = ("Unexpected error communicating with Beyonic API.")

        msg = textwrap.fill(msg) + "\n\n(error: " + str(e) + ")"
        raise BeyonicError(msg)


def get_default_http_client(*args, **kwargs):
    if urlfetch:
        impl = UrlFetchClient
    elif requests:
        impl = RequestsClient
    else:
        # none of them is available so let's throw an error
        raise BeyonicError(
            'Either of requests or urlfetch is not installed. Please install either of them using requirements.txt')

    return impl(*args, **kwargs)


'''
'API Client class interacts with api using available RequestClient or UrlFetchClient
'''


class ApiClient(object):
    """
    A client for the api
    """
    def __init__(self, api_key=None, url=None, client=None, verify_ssl_certs=True, api_version=None):
        # if not passed then let's try to get it from env variable
        if not api_key:
            try:
                api_key = os.environ['BEYONIC_ACCESS_KEY']
            except KeyError:
                raise BeyonicError('BEYONIC_ACCESS_KEY not set.')

        self._api_key = api_key
        self._api_version = api_version
        if not url:
            raise BeyonicError('Base url can\'t be empty. You should set base url using beyonic.api_endpoint_base')

        self._url = url
        self._client = client or get_default_http_client(verify_ssl_certs=verify_ssl_certs)

    def set_url(self, url):
        self._url = url

    def get(self, **kwargs):
        '''
        Makes an HTTP GET request to the  API. Any keyword arguments will
        be converted to query string parameters.
        '''
        return self._request("get", **kwargs)

    def post(self, **kwargs):
        '''
        Makes an HTTP POST request to the  API.
        '''
        return self._request("post", **kwargs)

    def put(self, **kwargs):
        '''
        Makes an HTTP PUT request to the  API.
        '''
        return self._request("put", **kwargs)

    def patch(self, **kwargs):
        '''
        Makes an HTTP patch request to the  API.
        '''
        return self._request("patch", **kwargs)

    def delete(self, **kwargs):
        '''
        Makes an HTTP DELETE request to the  API.
        '''
        return self._request("delete", **kwargs)

    def _request(self, method, **kwargs):
        response_content, status_code = self._client.request(
            method=method,
            url=self._url,
            headers=self._build_headers(),
            params=kwargs,
        )
        return self._parse_response(response_content, status_code)

    def _build_headers(self):
        headers = {}
        if self._api_key:
            headers.update({"Authorization": "Token %s" % self._api_key, })

        if self._api_version:
            headers.update({"Beyonic-Version": self._api_version, })

        headers.update({"Beyonic-Client": "Python", })
        headers.update({"Beyonic-Client-Version": beyonic.__version__, })

        return headers

    def _parse_response(self, response_content, status_code):
        # TODO: need exact status code for different type error
        if 200 <= status_code < 300:
            return self._value_for_response(response_content, status_code)
        else:
            raise self._exception_for_response(response_content, status_code)

    def _value_for_response(self, response_content, status_code):
        #status_code 204 is for delete so for it retruning True
        if response_content and status_code != 204:
            return GenericObject.from_json(response_content)
        else:
            return True

    def _exception_for_response(self, response_content, status_code):
        # TODO need to handle the all the status
        return ResponseError("%d error: %s" % (status_code, response_content,))




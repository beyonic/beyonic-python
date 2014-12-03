
import os
import urllib
from beyonic.api_client import ApiClient
from beyonic.resources import GenericObject

'''
' AbtractApi class, all the other api class extends it
'''
class AbstractAPI(GenericObject):

    @classmethod
    def get_client(cls, client=None):
        url = cls.get_url()
        from beyonic import api_key, verify_ssl_certs, api_version
        if client:
            return ApiClient(api_key=api_key, url=url, client=client, verify_ssl_certs=verify_ssl_certs, api_version=api_version)
        else:
            return ApiClient(api_key=api_key, url=url, client=None, verify_ssl_certs=verify_ssl_certs, api_version=api_version)

    @classmethod
    def get_url(cls):
        from beyonic import api_endpoint_base
        if not api_endpoint_base.endswith("/"):
            api_endpoint_base = api_endpoint_base + "/"
        cls_name = api_endpoint_base + str(cls._method_path)
        return cls_name

    @classmethod
    def list(cls, client=None):
        """
        This will return list of resorces.
        """
        return cls.get_client(client).get()

    @classmethod
    def create(cls, client=None, **kwargs):
        """
        This will return list of resorces.
        """
        return cls.get_client(client).post(**kwargs)
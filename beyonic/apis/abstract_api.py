from beyonic.api_client import ApiClient
from beyonic.resources import GenericObject
from beyonic.errors import BeyonicError


class AbstractAPI(GenericObject):
    """
    AbtractApi class, all the other api class extends it
    """
    @classmethod
    def get_client(cls, client=None):
        url = cls.get_url()
        from beyonic import api_key, verify_ssl_certs, api_version

        if client:
            return ApiClient(api_key=api_key, url=url, client=client, verify_ssl_certs=verify_ssl_certs,
                             api_version=api_version)
        else:
            return ApiClient(api_key=api_key, url=url, client=None, verify_ssl_certs=verify_ssl_certs,
                             api_version=api_version)

    @classmethod
    def get_url(cls):
        from beyonic import api_endpoint_base, DEFAULT_ENDPOINT_BASE

        if not api_endpoint_base:
            api_endpoint_base = DEFAULT_ENDPOINT_BASE

        if not api_endpoint_base.endswith("/"):
            api_endpoint_base = api_endpoint_base + "/"
        cls_name = api_endpoint_base + str(cls._method_path)
        return cls_name

    @classmethod
    def list(cls, client=None, **kwargs):
        """
        This will return list of resources.
        """
        objs = cls.get_client(client).get(**kwargs)

        #setting client object for each of the return object so that it can be used while saving data
        for obj in objs.results:
            if obj.id:
                base = cls.get_url()
                url = "%s/%s" % (base, obj.id)
                api_client = cls.get_client(client)
                api_client.set_url(url)
                obj.set_client(api_client)

        return objs

    @classmethod
    def create(cls, client=None, **kwargs):
        """
        This will create new object
        """
        return cls.get_client(client).post(**kwargs)

    @classmethod
    def get(cls, id, client=None, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise BeyonicError('Invalid ID or ID hasn\'t been specified')

        base = cls.get_url()
        url = "%s/%s" % (base, id)
        api_client = cls.get_client(client)
        api_client.set_url(url)
        obj = api_client.get(**kwargs)
        obj.set_client(api_client)
        return obj

    @classmethod
    def update(cls, id, client=None, **kwargs):
        """
        This will update the object
        """
        if not id:
            raise BeyonicError('Invalid ID or ID hasn\'t been specified')
        base = cls.get_url()
        url = "%s/%s" % (base, id)
        api_client = cls.get_client(client)
        api_client.set_url(url)
        return api_client.patch(**kwargs)

    @classmethod
    def delete(cls, id, client=None, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise BeyonicError('Invalid ID or ID hasn\'t been specified')

        base = cls.get_url()
        url = "%s/%s" % (base, id)
        api_client = cls.get_client(client)
        api_client.set_url(url)
        return api_client.delete(**kwargs)

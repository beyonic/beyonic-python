from beyonic.apis.abstract_api import AbstractAPI

'''
Collection api wrapper class
'''
class Collection(AbstractAPI):
    _method_path = 'collections'


class CollectionRequest(AbstractAPI):
    _method_path = 'collectionrequests'
# Beyonic API Python bindings

#default values if any
DEFAULT_ENDPOINT_BASE = 'https://app.beyonic.us/api/'

#config
api_key = None
api_endpoint_base = None
api_version = None
verify_ssl_certs = True #set to False if you want to bypass SSL checks(mostly useful while testing it on local env).


from beyonic.apis.payment import Payment
from beyonic.apis.webhook import Webhook
from beyonic.apis.collection import Collection
from beyonic.apis.collectionrequest import CollectionRequest
from beyonic.apis.account import Account
from beyonic.apis.contact import Contact
from beyonic.apis.transaction import Transaction

__version__ = "0.1.12"

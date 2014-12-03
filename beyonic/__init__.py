# Beyonic API Python bindings


#default values if any

#config
api_key = None
api_endpoint_base = None
api_version = None
verify_ssl_certs = True #set to False if you want to bypass SSL checks(mostly useful while testing it on local env).

from beyonic.apis.payment import Payment
from beyonic.apis.webhooks import Webhook
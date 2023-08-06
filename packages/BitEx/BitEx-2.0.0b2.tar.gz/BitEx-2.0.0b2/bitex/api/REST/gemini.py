# Import Built-ins
import logging
import json
import hashlib
import hmac
import base64

# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class GeminiREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://api.gemini.com' if not addr else addr
        version = 'v1' if not version else version
        super(GeminiREST, self).__init__(addr=addr, version=version, key=key,
                                         secret=secret, timeout=timeout,
                                         config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(GeminiREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)

        # Prepare Payload
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        payload = params
        payload['nonce'] = nonce
        payload['request'] = self.generate_uri(endpoint)
        payload = base64.b64encode(json.dumps(payload).encode('utf-8'))

        # generate signature
        sig = hmac.new(self.secret, payload, hashlib.sha384).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'X-GEMINI-APIKEY': self.key,
                                 'X-GEMINI-PAYLOAD': payload,
                                 'X-GEMINI-SIGNATURE': sig}
        return req_kwargs


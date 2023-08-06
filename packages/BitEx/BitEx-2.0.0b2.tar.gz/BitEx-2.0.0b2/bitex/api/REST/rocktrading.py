# Import Built-ins
import logging
import hashlib
import hmac


# Import Third-Party

# Import Homebrew# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class RockTradingREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        version = 'v1' if not version else version
        addr = 'https://api.therocktrading.com' if not addr else addr
        super(RockTradingREST, self).__init__(addr=addr, version=version,
                                              key=key, secret=secret,
                                              timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(RockTradingREST, self).sign_request_kwargs(endpoint,
                                                                      **kwargs)
        # Prepare Payload arguments
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}
        payload = params
        payload['nonce'] = int(nonce)
        #payload['request'] = self.generate_uri(endpoint)

        # generate signature
        msg = nonce + req_kwargs['url']
        sig = hmac.new(self.secret.encode(), msg.encode(),
                       hashlib.sha512).hexdigest()

        # Update req_kwargs keys
        req_kwargs['headers'] = {'X-TRT-KEY': self.key, 'X-TRT-Nonce': nonce,
                                 'X-TRT-SIGN': sig,
                                 'Content-Type': 'application/json'}
        req_kwargs['json'] = payload
        return req_kwargs



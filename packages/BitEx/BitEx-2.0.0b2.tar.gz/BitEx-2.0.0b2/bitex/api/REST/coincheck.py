# Import Built-ins
import logging
import json
import hashlib
import hmac

# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI


log = logging.getLogger(__name__)


class CoincheckREST(RESTAPI):
    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        addr = 'https://coincheck.com' if not addr else addr
        version = 'api' if not version else version
        super(CoincheckREST, self).__init__(addr=addr, version=version,
                                            key=key, secret=secret,
                                            timeout=timeout, config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        req_kwargs = super(CoincheckREST, self).sign_request_kwargs(endpoint,
                                                                    **kwargs)

        # Prepare argument for signature
        try:
            params = kwargs.pop('params')
        except KeyError:
            params = {}
        nonce = self.nonce()
        params = json.dumps(params)

        # Create signature
        # sig = nonce + url + req

        data = (nonce + req_kwargs['url'] + params).encode('utf-8')
        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha256)
        signature = h.hexdigest()

        # Update headers
        req_kwargs['headers'] = {"ACCESS-KEY": self.key,
                                 "ACCESS-NONCE": nonce,
                                 "ACCESS-SIGNATURE": signature}

        return req_kwargs

# Import Built-ins
import logging
import json
import hashlib
import hmac
import base64
import warnings

# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteCredentialConfigurationWarning

# Init Logging Facilities
log = logging.getLogger(__name__)


class ITbitREST(RESTAPI):
    def __init__(self, user_id=None, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        self.userId = user_id
        version = 'v1' if not version else version
        addr = 'https://api.itbit.com' if not addr else addr

        if user_id == '':
            raise ValueError("Invalid user id - cannot be empty string! "
                             "Pass None instead!")
        self.user_id = user_id
        super(ITbitREST, self).__init__(addr=addr, version=version, key=key,
                                        secret=secret, timeout=timeout,
                                        config=config)

    def check_auth_requirements(self):
        try:
            super(ITbitREST, self).check_auth_requirements()
        except IncompleteCredentialsError:
            raise

        if self.user_id is None:
            raise IncompleteCredentialsError
        else:
            return

    def load_config(self, fname):
        conf = super(ITbitREST, self).load_config(fname)
        try:
            self.user_id = conf['AUTH']['user_id']
        except KeyError:
            warnings.warn("'user_id' not found in config!",
                          IncompleteCredentialConfigurationWarning)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Requires that the HTTP request VERB is passed along in kwargs as
        as key:value pair 'method':<Verb>; otherwise authentication will
        not work.
        """
        req_kwargs = super(ITbitREST, self).sign_request_kwargs(endpoint,
                                                                **kwargs)

        # Prepare payload arguments
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        verb = kwargs['method']

        if verb in ('PUT', 'POST'):
            body = params
        else:
            body = {}

        timestamp = self.nonce()
        nonce = self.nonce()

        message = json.dumps([verb, req_kwargs['url'], body, nonce, timestamp],
                             separators=(',', ':'))
        sha256_hash = hashlib.sha256()
        nonced_message = nonce + message
        sha256_hash.update(nonced_message.encode('utf8'))
        hash_digest = sha256_hash.digest()
        hmac_digest = hmac.new(self.secret.encode('utf-8'),
                               req_kwargs['url'].encode('utf-8') + hash_digest,
                               hashlib.sha512).digest()
        signature = base64.b64encode(hmac_digest)

        # Update request kwargs header variable
        req_kwargs['headers'] = {'Authorization': self.key + ':' + signature.decode('utf8'),
                                 'X-Auth-Timestamp': timestamp,
                                 'X-Auth-Nonce': nonce,
                                 'Content-Type': 'application/json'}
        return req_kwargs


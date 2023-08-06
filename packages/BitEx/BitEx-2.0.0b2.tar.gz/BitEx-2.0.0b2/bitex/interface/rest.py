# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.utils import check_and_format_pair
from bitex.interface.base import Interface
from bitex.api import BaseAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class RESTAPI(BaseAPI):
    """
    Generic REST API interface. Supplies private and public query methods,
    as well as building blocks to customize the signature generation process.
    """
    def __init__(self, addr, timeout=None, key=None, secret=None, version=None,
                 config=None):
        """
        Initializes the RESTAPI instance.
        :param addr: str, API URL (excluding endpoint paths, if applicable)
        :param key: str, API key
        :param secret: str, API secret
        :param config: str, path to config file
        :param timeout: int or float, defines timeout for requests to API
        """
        super(RESTAPI, self).__init__(addr=addr, key=key, secret=secret,
                                      version=version, config=config)
        self.timeout = timeout if timeout else 10

    def generate_uri(self, endpoint):
        """
        Generates a Unique Resource Identifier (API Version + Endpoint)
        :param endpoint: str, endpoint path (i.e. /market/btcusd)
        :return: str, URI
        """
        if self.version:
            return '/' + self.version + '/' + endpoint
        else:
            return '/' + endpoint

    def generate_url(self, uri):
        """
        Generates a Unique Resource Locator (API Address + URI)
        :param uri: str, URI
        :return: str, URL
        """
        return self.addr + uri

    def sign_request_kwargs(self, endpoint, **kwargs):
        """
        Dummy Request Kwarg Signature Generator.
        Extend this to implement signing of requests for private api calls.
        By default, supplies a default URL using generate_uri and generate_url
        :param endpoint: str, API Endpoint
        :param kwargs: Kwargs meant for requests.Request()
        :return: dict, request kwargs
        """
        uri = self.generate_uri(endpoint)
        url = self.generate_url(uri)
        template = {'url': url, 'headers': {}, 'files': {},
                    'data': {}, 'params': {}, 'auth': {}, 'cookies': {},
                    'hooks': {}, 'json': {}}
        template.update(kwargs)
        return template

    def _query(self, method_verb, **request_kwargs):
        """
        Sends the request to the API via requests.
        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        resp = requests.request(method_verb, **request_kwargs,
                                timeout=self.timeout)
        #resp.raise_for_status()
        return resp

    def private_query(self, method_verb, endpoint, **request_kwargs):
        """Queries a private API endpoint requiring signing of the request.

        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param endpoint: str, API Endpoint
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        self.check_auth_requirements()
        request_kwargs = self.sign_request_kwargs(endpoint, **request_kwargs)
        return self._query(method_verb, **request_kwargs)

    def public_query(self, method_verb, endpoint, **request_kwargs):
        """
        Queries a public (i.e. unauthenticated) API endpoint and return the result.
        :param method_verb: valid HTTP Verb (GET, PUT, DELETE, etc.)
        :param endpoint: str, API Endpoint
        :param request_kwargs: kwargs for request.Request()
        :return: request.Response() object
        """
        request_kwargs['url'] = self.generate_url(self.generate_uri(endpoint))
        return self._query(method_verb, **request_kwargs)


class RESTInterface(Interface):
    def __init__(self, name, rest_api):
        super(RESTInterface, self).__init__(name=name, rest_api=rest_api)

    def _get_supported_pairs(self):
        return []

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        raise NotImplementedError

    # Private Endpoints
    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        raise NotImplementedError

    def open_orders(self, *args, **kwargs):
        raise NotImplementedError

    def cancel_order(self, *order_ids, **kwargs):
        raise NotImplementedError

    def wallet(self, *args, **kwargs):
        raise NotImplementedError

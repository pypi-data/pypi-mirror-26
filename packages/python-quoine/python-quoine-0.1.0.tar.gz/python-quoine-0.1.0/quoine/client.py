#!/usr/bin/env python
# coding=utf-8

import jwt
import requests
import six
import time

from .exceptions import QuoineAPIException, QuoineRequestException

if six.PY2:
    from urllib import urlencode
elif six.PY3:
    from urllib.parse import urlencode


class Quoine(object):

    API_URL = 'https://api.quoine.com'
    API_VERSION = '2'
    VENDOR_ID = None
    LANGUAGE = 'en'

    SIDE_BUY = 'buy'
    SIDE_SELL = 'sell'

    STATUS_FILLED = 'filled'
    STATUS_LIVE = 'live'
    STATUS_PARTIAL = 'partially_filled'
    STATUS_CANCELLED = 'cancelled'

    ORDER_TYPE_LIMIT = 'limit'
    ORDER_TYPE_MARKET = 'market'
    ORDER_TYPE_MARKET_RANGE = 'market_with_range'

    def __init__(self, api_token_id, api_secret, vendor_id=None, language=None):
        """Quoine API Client constructor

        :param api_token_id: Api Token Id
        :type api_token_id: str.
        :param api_secret: Api Secret
        :type api_secret: str.
        :param vendor_id: Vendor ID optional
        :type vendor_id: str.
        :param language: Langague optional
        :type language: str.

        """

        self.API_TOKEN_ID = api_token_id
        self.API_SECRET = api_secret
        if vendor_id:
            self.VENDOR_ID = vendor_id
        if language:
            self.LANGUAGE = language
        self.session = self._init_session()

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-quoine',
                   'X-Quoine-API-Version': self.API_VERSION,
                   'HTTP_ACCEPT_LANGUAGE': self.LANGUAGE,
                   'Accept-Language': self.LANGUAGE}
        if self.VENDOR_ID:
            headers['X-Quoine-Vendor-ID'] = self.VENDOR_ID
        session.headers.update(headers)
        return session

    def _generate_signature(self, path):

        auth_payload = {
            'path': path,
            'nonce': int(time.time() * 1000),
            'token_id': self.API_TOKEN_ID
        }

        return jwt.encode(auth_payload, self.API_SECRET, 'HS256')

    def _create_path(self, method, path, data):
        query_string = ''
        if method == 'get' and data:
            query_string = '?{}'.format(urlencode(data))
        return '/{}{}'.format(path, query_string)

    def _create_uri(self, path):
        return '{}{}'.format(self.API_URL, path)

    def _request(self, method, path, signed, **kwargs):

        kwargs['data'] = kwargs.get('data', {})
        kwargs['headers'] = kwargs.get('headers', {})

        path = self._create_path(method, path, kwargs['data'])
        uri = self._create_uri(path)

        if signed:
            # generate signature
            kwargs['headers']['X-Quoine-Auth'] = self._generate_signature(path)

        if kwargs['data'] and method == 'get':
            kwargs['params'] = kwargs['data']
            del(kwargs['data'])

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Quoine server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            raise QuoineAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise QuoineRequestException('Invalid Response: %s' % response.text)

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request('delete', path, signed, **kwargs)

    # Product Endpoints

    def get_products(self):
        """Get the list of all available products

        https://developers.quoine.com/#products

        :returns: list - List of product dictionaries

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                "id": 5,
                "product_type": "CurrencyPair",
                "code": "CASH",
                "name": "CASH Trading",
                "market_ask": "48203.05",
                "market_bid": "48188.15",
                "indicator": -1,
                "currency": "JPY",
                "currency_pair_code": "BTCJPY",
                "symbol": "¥",
                "fiat_minimum_withdraw": "1500.0",
                "pusher_channel": "product_cash_btcjpy_5",
                "taker_fee": "0.0",
                "maker_fee": "0.0",
                "low_market_bid": "47630.99",
                "high_market_ask": "48396.71",
                "volume_24h": "2915.627366519999999998",
                "last_price_24h": "48217.2",
                "last_traded_price": "48203.05",
                "last_traded_quantity": "1.0",
                "quoted_currency": "JPY",
                "base_currency": "BTC",
                "exchange_rate": "0.009398151671149725"
                },
                #...
            ]

        """

        return self._get('products')

    def get_product(self, product_id):
        """Get product details

        https://developers.quoine.com/#get-a-product

        :param product_id: required
        :type product_id: int

        :returns: list - List of product dictionaries

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 5,
                "product_type": "CurrencyPair",
                "code": "CASH",
                "name": "CASH Trading",
                "market_ask": "48203.05",
                "market_bid": "48188.15",
                "indicator": -1,
                "currency": "JPY",
                "currency_pair_code": "BTCJPY",
                "symbol": "¥",
                "fiat_minimum_withdraw": "1500.0",
                "pusher_channel": "product_cash_btcjpy_5",
                "taker_fee": "0.0",
                "maker_fee": "0.0",
                "low_market_bid": "47630.99",
                "high_market_ask": "48396.71",
                "volume_24h": "2915.62736652",
                "last_price_24h": "48217.2",
                "last_traded_price": "48203.05",
                "last_traded_quantity": "1.0",
                "quoted_currency": "JPY",
                "base_currency": "BTC",
                "exchange_rate": "0.009398151671149725"
            }

        """

        return self._get('products/{}'.format(product_id))

    def get_order_book(self, product_id, full=False):
        """Get order book for a product

        https://developers.quoine.com/#get-order-book

        :param product_id: required
        :type product_id: int
        :param full: default False, optional
        :type full: bool

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "buy_price_levels": [
                    [
                        "416.23000",    # price
                        "1.75000"       # amount
                    ],
                    #...
                ],
                "sell_price_levels": [
                    [
                        "416.47000",    # price
                        "0.28675"       # amount
                    ],
                    #...
                ]
            }

        """

        data = {'full': 1 if full else 0}
        return self._get('products/{}/price_levels'.format(product_id), data=data)

    # Excecution Endpoints

    def get_executions(self, product_id, limit=None, page=None):
        """Get a list of recent executions from a product (Executions are sorted in DESCENDING order - Latest first)

        https://developers.quoine.com/#executions

        :param product_id: required
        :type product_id: int
        :param limit: How many executions should be returned. Must be <= 1000. Default is 20
        :type limit: int
        :param page: From what page the executions should be returned, e.g if limit=20 and page=2, the response would start from the 21st execution. Default is 1
        :type page: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "models": [
                    {
                        "id": 1011880,
                        "quantity": "6.118954",
                        "price": "409.78",
                        "taker_side": "sell",
                        "created_at": 1457370745
                    },
                    {
                        "id": 1011791,
                        "quantity": "1.15",
                        "price": "409.12",
                        "taker_side": "sell",
                        "created_at": 1457365585
                    }
                ],
                "current_page": 2,
                "total_pages": 1686
            }

        """

        data = {
            'product_id': product_id
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page
        return self._get('executions', data=data)

    def get_executions_since_time(self, product_id, timestamp, limit=None):
        """Get a list of executions after a particular time (Executions are sorted in ASCENDING order)

        https://developers.quoine.com/#get-executions-by-timestamp

        :param product_id: required
        :type product_id: int
        :param timestamp: Only show executions at or after this timestamp
        :type timestamp: int (Unix timestamps in seconds)
        :param limit: How many executions should be returned. Must be <= 1000. Default is 20
        :type limit: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 960598,
                    "quantity": "5.6",
                    "price": "431.89",
                    "taker_side": "buy",
                    "created_at": 1456705487
                },
                {
                    "id": 960603,
                    "quantity": "0.06",
                    "price": "431.74",
                    "taker_side": "buy",
                    "created_at": 1456705564
                }
            ]

        """

        data = {
            'product_id': product_id,
            'timestamp': timestamp
        }
        if limit:
            data['limit'] = limit
        return self._get('executions', data=data)

    # Interest Rate Endpoints

    def get_interest_rate_ladder(self, currency):
        """Get a list of executions after a particular time (Executions are sorted in ASCENDING order)

        https://developers.quoine.com/#interest-rates

        :param currency: required (i.e. USD)
        :type currency: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "bids": [
                    [
                        "0.00020",
                        "23617.81698"
                    ],
                    [
                        "0.00040",
                        "50050.42000"
                    ],
                    [
                        "0.00050",
                        "100000.00000"
                    ]
                ],
                "asks": [
                ]
            }

        """

        return self._get('ir_ladders/{}'.format(currency))

    # Orders Endpoints

    def create_order(self, order_type, product_id, side, quantity, price=None, price_range=None):
        """Create a limit, market or market with range order

        https://developers.quoine.com/#orders

        :param order_type: required - limit, market or market_with_range
        :type order_type: string
        :param product_id: required
        :type product_id: int
        :param side: required - buy or sell
        :type side: string
        :param quantity: required quantity to buy or sell
        :type quantity: string
        :param price: required price per unit of cryptocurrency
        :type price: string
        :param price_range: optional For order_type of market_with_range only, slippage of the order.
        :type price_range: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "live",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD",
                "order_fee": "0.0",
                "margin_used": "0.0",
                "margin_interest": "0.0",
                "unwound_trade_leverage_level": null,
            }

        """

        data = {
            'order': {
                'order_type': order_type,
                'product_id': product_id,
                'side': side,
                'quantity': quantity
            }
        }
        if price and order_type == self.ORDER_TYPE_LIMIT:
            data['order']['price'] = price
        if price_range and order_type == self.ORDER_TYPE_MARKET_RANGE:
            data['order']['price_range'] = price_range
        return self._post('orders', True, json=data)

    def create_limit_buy(self, product_id, quantity, price):
        """Create a limit buy order

        https://developers.quoine.com/#orders

        :param product_id: required
        :type product_id: int
        :param quantity: required quantity to buy or sell
        :type quantity: string
        :param price: required price per unit of cryptocurrency
        :type price: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "live",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD",
                "order_fee": "0.0",
                "margin_used": "0.0",
                "margin_interest": "0.0",
                "unwound_trade_leverage_level": null,
            }

        """

        return self.create_order(self.ORDER_TYPE_LIMIT, product_id, self.SIDE_BUY, quantity, price)

    def create_limit_sell(self, product_id, quantity, price):
        """Create a limit sell order

        https://developers.quoine.com/#orders

        :param product_id: required
        :type product_id: int
        :param quantity: required quantity to buy or sell
        :type quantity: string
        :param price: required price per unit of cryptocurrency
        :type price: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "live",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD",
                "order_fee": "0.0",
                "margin_used": "0.0",
                "margin_interest": "0.0",
                "unwound_trade_leverage_level": null,
            }

        """

        return self.create_order(self.ORDER_TYPE_LIMIT, product_id, 'sell', quantity, price)

    def create_market_buy(self, product_id, quantity, price_range=None):
        """Create a market buy order

        https://developers.quoine.com/#orders

        :param product_id: required
        :type product_id: int
        :param quantity: required quantity to buy or sell
        :type quantity: string
        :param price_range: optional - slippage of the order.
        :type price_range: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "live",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD",
                "order_fee": "0.0",
                "margin_used": "0.0",
                "margin_interest": "0.0",
                "unwound_trade_leverage_level": null,
            }

        """

        order_type = self.ORDER_TYPE_MARKET
        if price_range:
            order_type = self.ORDER_TYPE_MARKET_RANGE
        return self.create_order(order_type, product_id, self.SIDE_BUY, quantity, price_range=price_range)

    def create_market_sell(self, product_id, quantity, price_range=None):
        """Create a market sell order

        https://developers.quoine.com/#orders

        :param product_id: required
        :type product_id: int
        :param quantity: required quantity to buy or sell
        :type quantity: string
        :param price_range: optional - slippage of the order.
        :type price_range: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "live",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD",
                "order_fee": "0.0",
                "margin_used": "0.0",
                "margin_interest": "0.0",
                "unwound_trade_leverage_level": null,
            }

        """

        order_type = self.ORDER_TYPE_MARKET
        if price_range:
            order_type = self.ORDER_TYPE_MARKET_RANGE
        return self.create_order(order_type, product_id, self.SIDE_SELL, quantity, price_range=price_range)

    def get_order(self, order_id):
        """Get an order

        https://developers.quoine.com/#get-an-order

        :param order_id: required
        :type order_id: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157479,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.01",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "filled",
                "leverage_level": 2,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD",
                "order_fee": "0.0",
                "margin_used": "0.0",
                "margin_interest": "0.0",
                "unwound_trade_leverage_level": null,
                "executions": [
                    {
                        "id": 4566133,
                        "quantity": "0.01",
                        "price": "500.0",
                        "taker_side": "buy",
                        "my_side": "sell",
                        "created_at": 1465396785
                    }
                ]
            }

        """

        return self._get('orders/{}'.format(order_id))

    def get_orders(self, funding_currency=None, product_id=None, status=None, with_details=False, limit=None, page=None):
        """Get a list of orders using filters

        https://developers.quoine.com/#get-orders

        :param funding_currency: optional - filter orders based on funding currency
        :type funding_currency: string
        :param product_id: optional - filter orders based on product
        :type product_id: int
        :param status: optional - filter orders based on status
        :type status: string
        :param with_details: optional - return full order details (attributes between \*) including executions
        :type with_details: bool
        :param limit: optional - page limit
        :type limit: int
        :param page: optional - page number
        :type page: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "models": [
                    {
                        "id": 2157474,
                        "order_type": "limit",
                        "quantity": "0.01",
                        "disc_quantity": "0.0",
                        "iceberg_total_quantity": "0.0",
                        "side": "sell",
                        "filled_quantity": "0.0",
                        "price": "500.0",
                        "created_at": 1462123639,
                        "updated_at": 1462123639,
                        "status": "live",
                        "leverage_level": 1,
                        "source_exchange": "QUOINE",
                        "product_id": 1,
                        "product_code": "CASH",
                        "funding_currency": "USD",
                        "currency_pair_code": "BTCUSD",
                        "unwound_trade_leverage_level": null,
                        "order_fee": "0.0",
                        "margin_used": "0.0",
                        "margin_interest": "0.0",
                        "executions": []
                    }
                ],
                "current_page": 1,
                "total_pages": 1
            }

        """

        data = {}
        if funding_currency:
            data['funding_currency'] = funding_currency
        if product_id:
            data['product_id'] = product_id
        if status:
            data['status'] = status
        if with_details:
            data['with_details'] = 1
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('orders', data=data)

    def cancel_order(self, order_id):
        """Cancel an order

        https://developers.quoine.com/#cancel-an-order

        :param order_id: required
        :type order_id: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "cancelled",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD"
            }

        """

        return self._put('orders/{}/cancel'.format(order_id))

    def update_live_order(self, order_id, quantity=None, price=None):
        """Update a live order

        https://developers.quoine.com/#edit-a-live-order

        :param order_id: required
        :type order_id: int
        :param quantity: optional - one or both of quantity or price should be set
        :type quantity: string
        :param price: optional - one or both of quantity or price should be set
        :type price: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 2157474,
                "order_type": "limit",
                "quantity": "0.01",
                "disc_quantity": "0.0",
                "iceberg_total_quantity": "0.0",
                "side": "sell",
                "filled_quantity": "0.0",
                "price": "500.0",
                "created_at": 1462123639,
                "updated_at": 1462123639,
                "status": "cancelled",
                "leverage_level": 1,
                "source_exchange": "QUOINE",
                "product_id": 1,
                "product_code": "CASH",
                "funding_currency": "USD",
                "currency_pair_code": "BTCUSD"
            }

        """

        data = {
            'order': {}
        }
        if quantity:
            data['order']['quantity'] = quantity
        if price:
            data['order']['price'] = price

        return self._put('orders/{}'.format(order_id), json=data)

    def get_order_trades(self, order_id):
        """Get an orders trades

        https://developers.quoine.com/#get-an-order's-trades

        :param order_id: required
        :type order_id: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 57896,
                    "currency_pair_code": "BTCUSD",
                    "status": "closed",
                    "side": "short",
                    "margin_used": "0.83588",
                    "open_quantity": "0.01",
                    "close_quantity": "0.0",
                    "quantity": "0.01",
                    "leverage_level": 5,
                    "product_code": "CASH",
                    "product_id": 1,
                    "open_price": "417.65",
                    "close_price": "417.0",
                    "trader_id": 3020,
                    "open_pnl": "0.0",
                    "close_pnl": "0.0065",
                    "pnl": "0.0065",
                    "stop_loss": "0.0",
                    "take_profit": "0.0",
                    "funding_currency": "USD",
                    "created_at": 1456250726,
                    "updated_at": 1456251837,
                    "close_fee": "0.0",
                    "total_interest": "0.02",
                    "daily_interest": "0.02"
                }
            ]

        """

        return self._get('orders/{}/trades'.format(order_id))

    # Executions Endpoints

    def get_my_executions(self, product_id, limit=None, page=None):
        """Get list of your executions

        https://developers.quoine.com/#get-your-executions

        :param product_id: required
        :type product_id: int
        :param limit: Limit execution per request
        :type limit: int
        :param page: Page
        :type page: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "models": [
                    {
                        "id": 1001232,
                        "quantity": "0.37153179",
                        "price": "390.0",
                        "taker_side": "sell",
                        "my_side": "sell",
                        "created_at": 1457193798
                    }
                ],
                "current_page": 1,
                "total_pages": 2
            }
        """

        data = {
            'product_id': product_id
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('executions/me', True, data=data)

    # Accounts Endpoints

    def get_fiat_accounts(self):
        """Get list of fiat accounts

        https://developers.quoine.com/#get-fiat-accounts

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 4695,
                    "currency": "USD",
                    "currency_symbol": "$",
                    "balance": "10000.1773",
                    "pusher_channel": "user_3020_account_usd",
                    "lowest_offer_interest_rate": "0.00020",
                    "highest_offer_interest_rate": "0.00060",
                    "exchange_rate": "1.0",
                    "currency_type": "fiat",
                    "margin": "0.0",
                    "free_margin": "10000.1773"
                }
            ]
        """

        return self._get('fiat_accounts', True)

    def create_fiat_account(self, currency):
        """Create a fiat account for a currency

        https://developers.quoine.com/#create-a-fiat-account

        :param currency: required
        :type currency: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 5595,
                "currency": "USD",
                "currency_symbol": "$",
                "balance": "0.0",
                "pusher_channel": "user_3122_account_usd",
                "lowest_offer_interest_rate": "0.00020",
                "highest_offer_interest_rate": "0.00060",
                "exchange_rate": "1.0",
                "currency_type": "fiat",
                "margin": "0.0",
                "free_margin": "0.0"
            }

        """
        data = {
            'currency': currency
        }
        return self._post('fiat_accounts', True, json=data)

    def get_crypto_accounts(self):
        """Get list of crypto accounts

        https://developers.quoine.com/#get-crypto-accounts

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 4668,
                    "balance": "4.99",
                    "address": "1F25zWAQ1BAAmppNxLV3KtK6aTNhxNg5Hg",
                    "currency": "BTC",
                    "currency_symbol": "฿",
                    "pusher_channel": "user_3020_account_btc",
                    "minimum_withdraw": 0.02,
                    "lowest_offer_interest_rate": "0.00049",
                    "highest_offer_interest_rate": "0.05000",
                    "currency_type": "crypto"
                }
            ]

        """

        return self._get('crypto_accounts', True)

    def get_account_balances(self):
        """Get all account balances

        https://developers.quoine.com/#get-all-account-balances

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "currency": "BTC",
                    "balance": "0.04925688"
                },
                {
                    "currency": "USD",
                    "balance": "7.17696"
                },
                {
                    "currency": "JPY",
                    "balance": "356.01377"
                }
            ]

        """

        return self._get('accounts/balance', True)

    # Assets Lending Endpoints

    def create_loan_bid(self, rate, quantity, currency):
        """Create a loan bid

        https://developers.quoine.com/#create-a-loan-bid

        :param rate: daily interest rate, e.g 0.0002 (0.02%), must be <= 0.07%
        :type rate: string
        :param quantity: amount to lend
        :type quantity: string
        :param currency: lending currency (all available in the system except JPY)
        :type currency: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 3580,
                "bidask_type": "limit",
                "quantity": "50.0",
                "currency": "USD",
                "side": "bid",
                "filled_quantity": "0.0",
                "status": "live",
                "rate": "0.0002",
                "user_id": 3020
            }

        """

        data = {
            'loan_bid': {
                'rate': rate,
                'quantity': quantity,
                'currency': currency
            }
        }

        return self._post('loan_bids', True, json=data)

    def get_loan_bid(self, currency, limit=None, page=None):
        """Get loan bids

        https://developers.quoine.com/#get-loan-bids

        :param currency: lending currency (all available in the system except JPY)
        :type currency: string
        :param limit: Limit execution per request
        :type limit: int
        :param page: Page
        :type page: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 3580,
                "bidask_type": "limit",
                "quantity": "50.0",
                "currency": "USD",
                "side": "bid",
                "filled_quantity": "0.0",
                "status": "live",
                "rate": "0.0002",
                "user_id": 3020
            }

        """

        data = {
            'currency': currency
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('loan_bids', True, data=data)

    def close_loan_bid(self, loan_bid_id):
        """Close loan bid

        https://developers.quoine.com/#close-loan-bid

        :param loan_bid_id: load bid Id
        :type loan_bid_id: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 3580,
                "bidask_type": "limit",
                "quantity": "50.0",
                "currency": "USD",
                "side": "bid",
                "filled_quantity": "0.0",
                "status": "closed",
                "rate": "0.0007",
                "user_id": 3020
            }

        """

        return self._put('loan_bids/{}/close'.format(loan_bid_id), True)

    def get_loans(self, currency, limit=None, page=None):
        """Get loans

        https://developers.quoine.com/#get-loans

        :param currency: lending currency (all available in the system except JPY)
        :type currency: string
        :param limit: Limit execution per request
        :type limit: int
        :param page: Page
        :type page: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "models": [
                    {
                        "id": 144825,
                        "quantity": "495.1048",
                        "rate": "0.0005",
                        "created_at": 1464168246,
                        "lender_id": 312,
                        "borrower_id": 5712,
                        "status": "open",
                        "currency": "JPY",
                        "fund_reloaned": true
                    }
                ],
                "current_page": 1,
                "total_pages": 1
            }

        """

        data = {
            'currency': currency
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('loans', True, data=data)

    def update_loan(self, loan_id, fund_reloaned=None):
        """Update a loan

        https://developers.quoine.com/#update-a-loan

        TODO: work out what else we can update

        :param loan_id: Loan Id
        :type loan_id: int
        :param fund_reloaned: optional
        :type fund_reloaned: bool

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 144825,
                "quantity": "495.1048",
                "rate": "0.0005",
                "created_at": 1464168246,
                "lender_id": 312,
                "borrower_id": 5712,
                "status": "open",
                "currency": "JPY",
                "fund_reloaned": false
            }

        """

        data = {
        }
        if fund_reloaned is not None:
            data['fund_reloaned'] = fund_reloaned

        return self._put('loans/{}'.format(loan_id), True, json=data)

    # Trading Accounts Endpoints

    def get_trading_accounts(self):
        """Get Trading Accounts

        https://developers.quoine.com/#get-trading-accounts

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 1759,
                    "leverage_level": 10,
                    "max_leverage_level": 10,
                    "pnl": "0.0",
                    "equity": "10000.1773",
                    "margin": "4.2302",
                    "free_margin": "9995.9471",
                    "trader_id": 4807,
                    "status": "active",
                    "product_code": "CASH",
                    "currency_pair_code": "BTCUSD",
                    "position": "0.1",
                    "balance": "10000.1773",
                    "created_at": 1421992165,
                    "updated_at": 1457242996,
                    "pusher_channel": "trading_account_1759",
                    "margin_percent": "0.1",
                    "product_id": 1,
                    "funding_currency": "USD",
                    "base_open_price": 0,
                    "long_summary": {
                        "pnl": "0.0",
                        "position": "0.0",
                        "base_open_price": "0.0"
                    },
                    "short_summary": {
                        "pnl": "0.0",
                        "position": "0.0",
                        "base_open_price": "0.0"
                    }
                },
                #...
            ]

        """

        return self._get('trading_accounts', True)

    def get_trading_account(self, account_id):
        """Get a Trading Account

        https://developers.quoine.com/#get-a-trading-account

        :param account_id: Trading Account Id
        :type account_id: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 1759,
                "leverage_level": 10,
                "max_leverage_level": 10,
                "pnl": "0.0",
                "equity": "10000.1773",
                "margin": "4.2302",
                "free_margin": "9995.9471",
                "trader_id": 4807,
                "status": "active",
                "product_code": "CASH",
                "currency_pair_code": "BTCUSD",
                "position": "0.1",
                "balance": "10000.1773",
                "created_at": 1421992165,
                "updated_at": 1457242996,
                "pusher_channel": "trading_account_1759",
                "margin_percent": "0.1",
                "product_id": 1,
                "funding_currency": "USD"
            }

        """

        return self._get('trading_accounts/{}'.format(account_id), True)

    def update_leverage_level(self, account_id, leverage_level):
        """Update Trading account leverage level

        https://developers.quoine.com/#update-leverage-level

        :param account_id: Trading Account Id
        :type account_id: int
        :param leverage_level: New leverage level
        :type leverage_level: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 1759,
                "leverage_level": 25,
                "max_leverage_level": 25,
                "pnl": "0.0",
                "equity": "10000.1773",
                "margin": "4.2302",
                "free_margin": "9995.9471",
                "trader_id": 4807,
                "status": "active",
                "product_code": "CASH",
                "currency_pair_code": "BTCUSD",
                "position": "0.1",
                "balance": "10000.1773",
                "created_at": 1421992165,
                "updated_at": 1457242996,
                "pusher_channel": "trading_account_1759",
                "margin_percent": "0.1",
                "product_id": 1,
                "funding_currency": "USD"
            }

        """

        data = {
            'trading_account': {
                'leverage_level': leverage_level
            }
        }

        return self._put('trading_accounts/{}'.format(account_id), True, json=data)

    # Trade Endpoints

    def get_trades(self, funding_currency=None, status=None, limit=None, page=None):
        """Get Trades

        https://developers.quoine.com/#get-trades

        :param funding_currency: optional - get trades of a particular funding currency
        :type funding_currency: string
        :param status: optional - open or closed
        :type status: string
        :param limit: Limit trades per request
        :type limit: int
        :param page: Page
        :type page: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "models": [
                    {
                        "id": 57896,
                        "currency_pair_code": "BTCUSD",
                        "status": "open",
                        "side": "short",
                        "margin_used": "0.83588",
                        "open_quantity": "0.01",
                        "close_quantity": "0.0",
                        "quantity": "0.01",
                        "leverage_level": 5,
                        "product_code": "CASH",
                        "product_id": 1,
                        "open_price": "417.65",
                        "close_price": "417.0",
                        "trader_id": 3020,
                        "open_pnl": "0.0",
                        "close_pnl": "0.0",
                        "pnl": "0.0065",
                        "stop_loss": "0.0",
                        "take_profit": "0.0",
                        "funding_currency": "USD",
                        "created_at": 1456250726,
                        "updated_at": 1456251837,
                        "close_fee": "0.0",
                        "total_interest": "0.02",
                        "daily_interest": "0.02"
                    },
                    #...
                ],
                "current_page": 1,
                "total_pages": 1
            }

        """

        data = {}
        if funding_currency:
            data['funding_currency'] = funding_currency
        if status:
            data['status'] = status
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('trades', True, data=data)

    def close_trade(self, trade_id, closed_quantity=None):
        """Close a trade

        https://developers.quoine.com/#close-a-trade

        :param trade_id: Trade Id
        :type trade_id: int
        :param closed_quantity: optional - The quantity you want to close
        :type closed_quantity: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 57896,
                "currency_pair_code": "BTCUSD",
                "status": "closed",
                "side": "short",
                "margin_used": "0.83588",
                "open_quantity": "0.01",
                "close_quantity": "0.0",
                "quantity": "0.01",
                "leverage_level": 5,
                "product_code": "CASH",
                "product_id": 1,
                "open_price": "417.65",
                "close_price": "417.0",
                "trader_id": 3020,
                "open_pnl": "0.0",
                "close_pnl": "0.0065",
                "pnl": "0.0065",
                "stop_loss": "0.0",
                "take_profit": "0.0",
                "funding_currency": "USD",
                "created_at": 1456250726,
                "updated_at": 1456251837,
                "close_fee": "0.0",
                "total_interest": "0.02",
                "daily_interest": "0.02"
            }

        """

        data = {}
        if closed_quantity:
            data['closed_quantity'] = closed_quantity

        return self._put('trades/{}/close'.format(trade_id), True, json=data)

    def close_all_trades(self, side=None):
        """Close all trades

        https://developers.quoine.com/#close-all-trade

        :param side: optional - Close all trades of this side. Close trades of both side if left blank
        :type side: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 57896,
                    "currency_pair_code": "BTCUSD",
                    "status": "closed",
                    "side": "short",
                    "margin_used": "0.83588",
                    "open_quantity": "0.01",
                    "close_quantity": "0.0",
                    "quantity": "0.01",
                    "leverage_level": 5,
                    "product_code": "CASH",
                    "product_id": 1,
                    "open_price": "417.65",
                    "close_price": "417.0",
                    "trader_id": 3020,
                    "open_pnl": "0.0",
                    "close_pnl": "0.0065",
                    "pnl": "0.0065",
                    "stop_loss": "0.0",
                    "take_profit": "0.0",
                    "funding_currency": "USD",
                    "created_at": 1456250726,
                    "updated_at": 1456251837,
                    "close_fee": "0.0",
                    "total_interest": "0.02",
                    "daily_interest": "0.02"
                }
            ]

        """

        data = {}
        if side:
            data['side'] = side

        return self._put('trades/close_all', True, json=data)

    def update_trade(self, trade_id, stop_loss, take_profit):
        """Update a trade

        https://developers.quoine.com/#update-a-trade

        :param trade_id: Trade Id
        :type trade_id: int
        :param stop_loss: Stop Loss price
        :type stop_loss: string
        :param take_profit: Take Profit price
        :type take_profit: string

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            {
                "id": 57897,
                "currency_pair_code": "BTCUSD",
                "status": "open",
                "side": "short",
                "margin_used": "0.83588",
                "open_quantity": "0.01",
                "close_quantity": "0.0",
                "quantity": "0.01",
                "leverage_level": 5,
                "product_code": "CASH",
                "product_id": 1,
                "open_price": "417.65",
                "close_price": "0",
                "trader_id": 3020,
                "open_pnl": "0.0",
                "close_pnl": "0.0065",
                "pnl": "0.0065",
                "stop_loss": "300.0",
                "take_profit": "600.0",
                "funding_currency": "USD",
                "created_at": 1456250726,
                "updated_at": 1456251837,
                "close_fee": "0.0",
                "total_interest": "0.02",
                "daily_interest": "0.02"
            }

        """

        data = {
            'trade': {
                'stop_loss': stop_loss,
                'take_profit': take_profit
            }
        }

        return self._put('trades/{}'.format(trade_id), True, json=data)

    def get_trade_loans(self, trade_id):
        """Get a trade's loans

        https://developers.quoine.com/#get-a-trade's-loans

        :param trade_id: Trade Id
        :type trade_id: int

        :returns: API response

        :raises: QuoineResponseException, QuoineAPIException

        .. code-block:: python

            [
                {
                    "id": 103520,
                    "quantity": "42.302",
                    "rate": "0.0002",
                    "created_at": 1461998432,
                    "lender_id": 100,
                    "borrower_id": 3020,
                    "status": "open",
                    "currency": "USD",
                    "fund_reloaned": true
                }
            ]

        """

        return self._get('trades/{}/loans'.format(trade_id), True)


class Quoinex(Quoine):
    pass


class Qryptos(Quoinex):
    API_URL = 'https://api.qryptos.com'

import requests
import asyncio
import aiohttp
import json
# import websockets

from .default_collector import BaseCollector
from tweakers_coin_db.database import db_session
from datetime import datetime

class UpbitCollector(BaseCollector):

    def __init__(self, log_instance=None, db_session=db_session):
        self.base_url = "https://api.upbit.com/v1"
        self.crix_base_url = "https://crix-api-cdn.upbit.com/v1/crix"

        self.db_session = db_session
        self.market_pairs = None
        self.marking = 'upbit.api'
        super().__init__(self.db_session, log_instance, self.base_url)


# https://crix-api-cdn.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-ETH&count=200&ciqrandom=1546522918045

    async def _async_get_ohlc(self, client, candle_type, market, to='', count=200, minute=None):
        if client is None:
            raise ValueError("check client")

        accept_candle = (
            'min' , 'day', 'week', 'month'
        )
        accept_minute = (
            '1', '3', '5', '10', '15', '30', '60', '240',
        )

        if candle_type in accept_candle or not market:
            if candle_type == 'min':
                if minute in accept_minute:
                    candle_type = '/minutes/' + minute
                else:
                    raise ValueError("check minute")
            else:
                candle_type  = '/' + candle_type
        else:
            raise ValueError('check period')

        if to:
            to = self.convert_timestamp_to_iso(to)

        ex_url = '/candles'
        url = '%s%s%s' % (self.crix_base_url,ex_url, candle_type)
        url = '%s?code=CRIX.UPBIT.%s&to=%s&count=%s' % (url, market, to, count)
        # print(url)
        response = await self._async_request_url(url, client)
        parsed_json = json.loads(response)
        return parsed_json

    def _get_ohlc(self, candle_type, market, to='', count=200, minute=None):
        accept_candle = (
            'min' , 'day', 'week', 'month'
        )
        accept_minute = (
            '1', '3', '5', '10', '15', '30', '60', '240',
        )

        if candle_type in accept_candle or not market:
            if candle_type == 'min':
                if minute in accept_minute:
                    candle_type = '/minutes/' + minute
                else:
                    raise ValueError("minute를 넣어주세요")
            else:
                candle_type  = '/' + candle_type
        else:
            raise ValueError('장난??? accept period 확인해라')

        if to:
            to = self.convert_timestamp_to_iso(to)

        ex_url = '/candles'
        url = '%s%s%s' % (self.base_url,ex_url, candle_type)
        url = '%s?market=%s&to=%s&count=%s' % (url, market, to, count)
        # print(url)
        response = self._request_url(url)
        return response.json()

    def _get_market(self, symbol=''):
        ex_url = '/market/all'

        url = "%s%s" % (self.base_url, ex_url)
        print(url)
        response = self._request_url(url)
        return response.json()

    def _get_pairs(self):
        return self._get_market()

    def get_all_markets(self):
        return self._get_market()

    def convert_timestamp_to_iso(self, timestamp):
        return datetime.fromtimestamp(timestamp).isoformat() + 'Z'

    def convert_iso_to_timestamp(self, isoformat):
        return int(datetime.fromisoformat(isoformat).timestamp())

    def _current_timestamp(self):
        return int(datetime.now().timestamp())

    def _current_isoformat(self):
        return datetime.now().isoformat() + "Z"

    
import requests
import aiohttp
import asyncio
import time

from pprint import pprint
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tweakers_coin_db.database.models.collector import Exchanges, Currency, CryptoMarket


class BaseCollector(object):
    api_base = "https://api.cryptowat.ch"

    # exchange -> https://api.cryptowat.ch/exchanges/<거래소이름>
    # currency : https://api.cryptowat.ch/assets/<usd등 currency정보>
    # base_quote를 위한 pair정보 -> https://api.cryptowat.ch/pairs/<symbol정보>
    # crypto_symbol(markets) : https://api.cryptowat.ch/<markets>/<거래소이름>/<symbol정보>/<options [price, summary, orderbook,trades,ohlc]>
    # ohlcv : https://api.cryptowat.ch/markets/<거래소 이름>/<pair정보>/ohlc?

    # [util]
    # 여러개 serialize

    # [공통] - Base Crypto Class
    # 0.0 반드시 필수기능: [[url request, db저장]에 로그 남기기, 에러발생시 로그 남기기]
    # 0.1 현재 가능한 거래소들 조회하고 상태 변경시(db에 저장하기)
    # [api 기능] - Inherited class
    # 1. currency -> 현재 api에서 실시간으로 이용가능한 currency 확인후, db update하기 (currency 함수)
    # 2. pairs -> 거래가능한 pair들을 조회한다. 해당 링크에 [route]링크가 있으며 그 링크는 해당 페어를 지원하는 마켓으로 연결한다. (pairs 함수)
    # 3. exchange -> 거래소를 조회한다. route링크로 조회한다. 세부 거래소로 갈 수 있으며 그 세부거래소에서 [route링크]로  market으로 연결된다.
    # 4. market -> (전체 호출시)마켓 상태를 확인한다, [option]까지 조회시 세부사항을 얻을 수 있다.
    # 5. OHLC -> 차트 데이터를 얻는다.

    # def __init__(self, log_instance=None, base_url=None):
    #     self.logger = log_instance
    #     self.base_url=base_url


    def __init__(self, db_session, log_instance, base_url):
        self.logger = log_instance
        self.db_session = db_session
        self.base_url = base_url

    def _request_url(self, url):
        response = requests.get(url)
        # TODO 로그 남기기
        if self.logger:
            self.logger.info("- {} request요청 \n {} \n".format(self.__class__.__name__, url))
        status_code = response.status_code
        return response

    async def _async_request_url(self, url, client):
        # time.sleep(0.1)
        headers = {"user-agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
                    "origin" : "https://upbit.com",
                    ":authority": "crix-api-cdn.upbit.com"}

        async with client.get(url, headers=headers) as response:
            self.logger.info("- {} request요청 \n {} \n".format(self.__class__.__name__, url))
            if response.status != 200:
                result = await response.read()
                self.logger.error("- {} \n request url : {} error has occured \n contents : {} .".format(self.__class__.__name__, url, result))
            assert response.status == 200
            result = await response.read()
        return result

    def _get_currency_info(self, url):

        pass

    def _get_pairs(self, url):
        pass

    def _get_exchange(self,url):
        pass

    def _get_market(self, url):
        pass

    def _get_ohlc(self,url):
        pass


    def fetch_all(self):
        pass
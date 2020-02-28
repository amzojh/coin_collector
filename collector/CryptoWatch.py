	import requests

	from .default_collector import BaseCollector
	from tweakers_coin_db.database import db_session

	class CryptoWatchCollector(BaseCollector):
		# 현재 가격 조회하기 viewing

		# 0.1 현재 가능한 거래소들 조회하고 상태 변경시(db에 저장하기)
		# [api 기능]
		# 1. asset -> 현재 api에서 실시간으로 이용가능한 currency 확인후, db update하기 (currency 함수)
		# 2. pairs -> 거래가능한 pair들을 조회한다. 해당 링크에 [route]링크가 있으며 그 링크는 해당 페어를 지원하는 마켓으로 연결한다. (pairs 함수)
		# 3. exchange -> 거래소를 조회한다. route링크로 조회한다. 세부 거래소로 갈 수 있으며 그 세부거래소에서 [route링크]로  market으로 연결된다.
		# 4. market -> (전체 호출시)마켓 상태를 확인한다, [option]까지 조회시 세부사항을 얻을 수 있다.
		# 5. OHLC -> 차트 데이터를 얻는다.
		###TODO    [1.exchange data넣기, 2.pair 넣기, 3.ohlc넣기]

		def __init__(self, log_instance=None, db_session=db_session):
			self.market_pairs = None
			self.db_session = db_session
			self.base_url = "https://api.cryptowat.ch"
			super().__init__(self.db_session, log_instance, self.base_url)

		def get_assets(self, symbol=''):
			ex_url = '/assets'
			if symbol:
				symbol = '/' + symbol

			url = "%s%s%s" % (self.base_url, ex_url, symbol)

			response = self._request_url(url)

			return response.json()

		def get_all_assets(self):
			return self.get_assets()

		# def get_market(self):
		# 	return self.
		def get_exchange(self, exchange_name=''):
			ex_url = '/exchanges'
			exchange_name = exchange_name.lower()

			if exchange_name:
				exchange_name = '/' + exchange_name

			url = "%s%s%s" % (self.base_url, ex_url, exchange_name)
			response = self._request_url(url)

			return response.json()

		def get_all_exchange(self):
			return self.get_exchange()

		def get_market(self, market=''):
			ex_url = '/markets'
			market = market.lower()

			if market:
				market = '/' + market

			url = "%s%s%s" % (self.base_url, ex_url, market)

			response = self._request_url(url)

			return response.json()

		def get_all_market(self):
			return self.get_market()

		def get_pairs(self, pair=''):
			ex_url = "/pairs"
			pair = pair.lower()

			if pair:
				pair = '/' + pair

			url = "%s%s%s" % (self.base_url, ex_url, pair)
			response = self._request_url(url)

			return response.json()

		def get_all_pairs(self):
			return self.get_pairs()

		def get_ohlc(self, exchange=None, pair=None, before='', after='', periods='60'):
			accept_periods = (
				'60', '180', '300', '900', '1800', '3600', '7200', '14400', '21600', '43200', '86400', '259200', '604800')
			if periods not in accept_periods or not exchange or not pair:
				raise ValueError('check period')

			ex_url = '/markets'

			url = "%s%s/%s/%s/ohlc" % (self.base_url, ex_url, exchange, pair)

			url = "%s?before=%s&after=%s&periods=%s" % (url, before, after, periods)
			print(url)
			response = self._request_url(url)
			return response.json()

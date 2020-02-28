import os
import sys
import datetime

from pprint import pprint
import time
import logging
import asyncio
import aiohttp

from sqlalchemy import text
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import insert

from collector.CryptoWatch import CryptoWatchCollector
from collector.upbit import UpbitCollector
from tweakers_coin_db.database import db_session, Session, engine
from tweakers_coin_db.database.models import Candle1M, Candle3M, Candle5M, Candle15M, Candle30M, Candle1H, Candle2H, \
	Candle4H, Candle6H, Candle12H, Candle1D, Candle3D, Candle1W, Candle4W
from tweakers_coin_db.database.models import CryptoMarket, Upbit


class CrawlerLogger():
	_logger = None
	
	def __init__(self):
		crawler_logger = logging.getLogger('crawler_logger')
		log_file_path = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.log'
		
		if not os.path.exists(os.getcwd() + '/log/error'):
			os.makedirs(os.getcwd() + '/log/error')


		formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

		file_handler = logging.FileHandler(filename=os.path.join(os.getcwd() + '/log', log_file_path), mode='w')
		file_handler.setLevel(logging.INFO)
		file_handler.setFormatter(formatter)

		error_file_handler = logging.FileHandler(filename=os.path.join(os.getcwd() + '/log/error', log_file_path), mode='w')
		error_file_handler.setLevel(logging.ERROR)
		error_file_handler.setFormatter(formatter)

		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.setLevel(logging.INFO)
		stream_handler.setFormatter(formatter)
		crawler_logger.setLevel(logging.INFO)
		crawler_logger.addHandler(file_handler)
		crawler_logger.addHandler(stream_handler)
		crawler_logger.addHandler(error_file_handler)
		self._logger = crawler_logger
	
	def get_logger(self):
		return self._logger

class Collector(object):
	logger = CrawlerLogger()
	crypto_collector = CryptoWatchCollector()
	upbit_collector = UpbitCollector(log_instance=logger.get_logger())

	def cryptoWatch_collect_all_assets(self):
		assets_json = self.crypto_collector.get_all_assets()
		# self.crypto_collector.get_assets() 과 동일

		result_assets = assets_json.get('result', None)
		# start_time = time.time()

		sql_set = set()
		for asset in result_assets:
			sql_set.add(
				(asset['name'], asset['symbol'].lower(), bool(asset['fiat']))
			)
		sql_str = repr(sql_set)[1:-1]
	
		# for문 돌리면 15초 정도
		# sql tuning 후 0.4초

		sql = "INSERT INTO currency (currency_name,currency_symbol,is_fiat) " \
			  "VALUES %s ON DUPLICATE KEY UPDATE currency_name=VALUES(currency_name),is_fiat=VALUES(is_fiat);" % sql_str

		self.crypto_collector.db_session.execute(sql)
		self.crypto_collector.commit()

	def collect_all_assets(self):
		self.cryptoWatch_collect_all_assets()


	def cryptoWatch_collect_exchange(self):
		exchangies_json = self.crypto_collector.get_all_exchange()
		result_exchangies = exchangies_json.get('result', None)

		sql_set = set()
		for exchange in result_exchangies:
			sql_set.add(
				(exchange['name'], exchange['symbol'].lower())
			)

		sql_str = repr(sql_set)[1:-1]
		sql = "INSERT INTO exchanges (exchange_name,exchange_symbol) " \
			  "VALUES %s ON DUPLICATE KEY UPDATE exchange_name=VALUES(exchange_name);" % sql_str

		self.crypto_collector.db_session.execute(sql)
		self.crypto_collector.db_session.commit()

	def collect_all_exchange(self):
		self.cryptoWatch_collect_all_assets()



	def cryptoWatch_collect_marketpair(self):
		# pair에 대한 base와 quote를 입력
		marketpair_json = self.crypto_collector.get_all_market()
		result_marketpair = marketpair_json.get('result', None)

		sql_set = set()
		for marketpair in result_marketpair:
			sql_set.add(
				(marketpair['pair'], marketpair['exchange'], 'cryptowat.ch')
			)

		sql_str = repr(sql_set)[1:-1]
		sql = "INSERT INTO cryptomarket (crypto_pair, crypto_exchange, api_src) " \
			  "VALUES %s ON DUPLICATE KEY UPDATE crypto_pair=VALUES(crypto_pair), crypto_exchange=VALUES(crypto_exchange), api_src=VALUES (api_src);" % sql_str

		self.crypto_collector.db_session.execute(sql)
		self.crypto_collector.db_session.commit()

	def upbit_collect_crypto_pair(self):
		pair_list = self.upbit_collector._get_pairs()
		sql_set = set()
		for pair in pair_list:
			pair_data = pair['market'].lower().replace('-', '')
			sql_set.add(``
				(pair['market'], pair_data)
            )
		sql_str = repr(sql_set)[1:-1]
		sql = "INSERT INTO upbit_pair (original_symbol, symbol) " \
              "VALUES %s ON DUPLICATE KEY UPDATE original_symbol=VALUES(original_symbol), symbol=VALUES(symbol);" % sql_str

		self.upbit_collector.db_session.execute(sql)
		self.upbit_collector.db_session.commit()


	def upbit_collect_marketpair(self):
		pairs_json = self.upbit_collector.get_all_markets()
		sql_set = set()
		for pair in pairs_json:
			pair_data = pair['market'].lower().replace('-', '')
			sql_set.add(
				(pair_data, 'upbit', 'api.upbit')
			)
		sql_str = repr(sql_set)[1:-1]
		print(sql_str)
		sql = "INSERT INTO cryptomarket (crypto_pair, crypto_exchange, api_src )" \
			  "VALUES %s ON DUPLICATE KEY UPDATE crypto_pair=VALUES(crypto_pair), crypto_exchange=VALUES (crypto_exchange), api_src =VALUES (api_src) " % sql_str

		self.upbit_collector.db_session.execute(sql)
		self.upbit_collector.db_session.commit()


	def collect_all_marketpair(self):
		self.cryptoWatch_collect_marketpair()
		self.upbit_collect_marketpair()


	def cryptoWatch_collect_pair(self):
		pairs_json = self.crypto_collector.get_all_pairs()
		result_pairs = pairs_json.get('result', None)

		sql_set = set()

		for pair in result_pairs:
			sql_set.add(
				(pair['base']['symbol'], pair['quote']['symbol'])
			)
		sql_str = repr(sql_set)[1:-1]

		sql = "INSERT INTO cryptopair (base_currency, quote_currency) " \
			  "VALUES %s ON DUPLICATE KEY UPDATE base_currency=VALUES(base_currency), quote_currency=VALUES(quote_currency);" % sql_str

		self.crypto_collector.db_session.execute(sql)
		self.crypto_collector.db_session.commit()

	def collect_all_pair(self):
		self.cryptoWatch_collect_pair()



	def upbit_collect_ohlc(self):
		market_pairs = CryptoMarket.query.filter_by(crypto_exchange="upbit").all()
		# origin_pairs = self.upbit_collector.db_session.query(Upbit).join(CryptoMarket).filter(Upbit.symbol == CryptoMarket.crypto_pair).all()
		origin_pairs = self.upbit_collector.db_session.query(Upbit).all()
		pprint(origin_pairs[3].original_symbol)
		query_param_pair = {}
		for origin_pair in origin_pairs:
			query_param_pair[origin_pair.symbol] = origin_pair.original_symbol

		pprint(query_param_pair)

		candle_list = [Candle1M]
			# , Candle3M, Candle5M, Candle15M, Candle30M, Candle1H,
			# 		   Candle4H, Candle1D, Candle1W, Candle4W]

		count = 0
		for candle_cls in candle_list:
			print("***", candle_cls.__name__, "를 시작합니다")
			for market_pair in market_pairs:
				print("**", market_pair, "를 시작합니다.")

				current_time = self.upbit_collector._current_timestamp()
				print(current_time)
				minute = str(int(candle_cls._seconds / 60))
				first_candle = candle_cls.query.filter_by(
					crypto_exchange=market_pair.crypto_exchange, crypto_pair=market_pair.crypto_pair
				).order_by(candle_cls.time_stamp.desc()).first()  # 내림차순으로 가져옴
                
				last_candle = candle_cls.query.filter_by(
					crypto_exchange=market_pair.crypto_exchange, crypto_pair=market_pair.crypto_pair
				).order_by(candle_cls.time_stamp).first()  # 내림차순으로 가져옴
				second_current_time = int(last_candle.time_stamp) + 60 * 200

				for i in range(3):
					count += 1
					if first_candle and (current_time - first_candle.time_stamp) < candle_cls._seconds:
						print(candle_cls.crypto_pair, "최신 데이터 업데이트 완료")
						break
					ohlc_jsons = self.upbit_collector.get_ohlc(
						candle_type=candle_cls._type,
						market=query_param_pair[market_pair.crypto_pair],
						to=current_time,
						count=200,
						minute=minute
					)
					current_time = current_time - 60 * ohlc_jsons.__len__()
					sql_set = set()
					sql_set = self.upbit_parse_ohlc(ohlc_jsons, sql_set, market_pair)
					self.upbit_ohlc_commit(candle_cls.__tablename__, sql_set)


	async def async_upbit_collect_historical_ohlc(self, client):
		market_pairs = CryptoMarket.query.filter_by(crypto_exchange="upbit").filter(CryptoMarket.crypto_pair.like('%krw%'), CryptoMarket.update_completed!='Y').all()
		print(market_pairs)
		origin_pairs = self.upbit_collector.db_session.query(Upbit).filter(Upbit.symbol.like('%krw%')).all()
		# pprint(origin_pairs[3].original_symbol)
		query_param_pair = {}
		for origin_pair in origin_pairs:
			query_param_pair[origin_pair.symbol] = origin_pair.original_symbol

		pprint(query_param_pair)	

		candle_list = [Candle1M]
		count = 0
		task_list = []
		for candle_cls in candle_list:
			print("***", candle_cls.__name__, "를 시작합니다")
			for market_pair in market_pairs:
				print("**", market_pair, "를 시작합니다.")

				current_time = self.upbit_collector._current_timestamp()
				minute = str(int(candle_cls._seconds / 60))
				task = asyncio.ensure_future(self.async_get_historical_ohlc_process(candle_cls, current_time, market_pair, query_param_pair, minute, client))
				task_list.append(task)

		return_list = await asyncio.gather(*task_list)
		await self.async_get_upbit_ohlc_commit_process(return_list)
		await client.close()

	async def async_upbit_collect_current_ohlc(self, client):
		market_pairs = CryptoMarket.query.filter_by(crypto_exchange="upbit").filter(CryptoMarket.crypto_pair.like('%krw%')).all()
		print(market_pairs)
		origin_pairs = self.upbit_collector.db_session.query(Upbit).filter(Upbit.symbol.like('%krw%')).all()
		# pprint(origin_pairs[3].original_symbol)
		query_param_pair = {}
		for origin_pair in origin_pairs:
			query_param_pair[origin_pair.symbol] = origin_pair.original_symbol

		pprint(query_param_pair)

		candle_list = [Candle1M]
		count = 0
		task_list = []
		for candle_cls in candle_list:
			print("***", candle_cls.__name__, "를 시작합니다")
			for market_pair in market_pairs:
				print("**", market_pair, "를 시작합니다.")

				current_time = self.upbit_collector._current_timestamp()
				minute = str(int(candle_cls._seconds / 60))
				task = asyncio.ensure_future(self.async_get_current_ohlc_process(candle_cls, current_time, market_pair, query_param_pair, minute, client))
				task_list.append(task)

		return_list = await asyncio.gather(*task_list)
		await self.async_get_upbit_ohlc_commit_process(return_list)
		await client.close()

		
	async def async_get_upbit_ohlc_commit_process(self, result_list):
			for result in result_list:
				if not result["updated_or_not"]:
					updated_row = CryptoMarket.query.filter_by(
						crypto_exchange=result["market_info"].crypto_exchange,
						crypto_pair=result["market_info"].crypto_pair,
						api_src="api.upbit"
					).one()
					updated_row.update_completed = 'Y'
					self.upbit_collector.db_session.commit()
				else:
					await self.async_upbit_ohlc_commit(result["data"], result["table_name"])

	async def async_get_historical_ohlc_process(self, candle_cls, current_time, market_pair, query_param_pair, minute, client):
		sql_query_set = set()
		last_candle = candle_cls.query.filter_by(
			crypto_exchange=market_pair.crypto_exchange, crypto_pair=market_pair.crypto_pair
		).order_by(candle_cls.time_stamp).first()  # 내림차순으로 가져옴
		current_time = 0 
		lowest_timestamp = 0
		if last_candle is None:
			# default로 2019년 1월 1일로 세팅
			current_time = 1546300800
			lowest_timestamp = 1546300800
		else:
			current_time = last_candle.time_stamp
			lowest_timestamp = last_candle.time_stamp
		requested_data_count = 0
		count = 0
		while count < 20 and 1483185600 < current_time - requested_data_count * 60:
			print("count" , count)
			count += 1
			ohlc_jsons = await self.upbit_collector._async_get_ohlc(
				candle_type=candle_cls._type,
				market=query_param_pair[market_pair.crypto_pair],
				to=current_time - requested_data_count * candle_cls._seconds,
				count=200,
				minute=minute,
				client=client
			)
			requested_data_count += len(ohlc_jsons)
			sql_set = set()
			sql_set, lowest_timestamp = self.upbit_parse_ohlc(ohlc_jsons, sql_set, market_pair, lowest_timestamp)
			sql_query_set = sql_query_set.union(sql_set)
		
		updated_or_not = True
		if last_candle != None:
			print(f"symbol : {last_candle.crypto_pair}\nlast timestamp : {lowest_timestamp} and current timestamp : {last_candle.time_stamp}")
		
		if last_candle != None and lowest_timestamp == last_candle.time_stamp and count > 1:
			self.upbit_collector.logger.warning(f'symbol : {query_param_pair[market_pair.crypto_pair]} is not needed to update anymore' )
			updated_or_not = False

		return {"data" : sql_query_set, "table_name" : candle_cls.__tablename__, "updated_or_not" : updated_or_not, "market_info" : last_candle}

	async def async_get_current_ohlc_process(self, candle_cls, current_time, market_pair, query_param_pair, minute, client):
		sql_query_set = set()
		first_candle = candle_cls.query.filter_by(
			crypto_exchange=market_pair.crypto_exchange, crypto_pair=market_pair.crypto_pair
		).order_by(candle_cls.time_stamp.desc()).first()  # 내림차순으로 가져옴

		current_time = 0
		highest_time = self.upbit_collector._current_timestamp()
		if first_candle is None:
			current_time = 1546300800
		else:
			current_time = first_candle.time_stamp

		count = 0
		while count < 3:
			count += 1
			if current_time - highest_time > candle_cls._seconds:
				print(candle_cls.crypto_pair, "최신 데이터 업데이트 완료")
				break
			
			ohlc_jsons = await self.upbit_collector._async_get_ohlc(
				candle_type=candle_cls._type,
				market=query_param_pair[market_pair.crypto_pair],
				to=current_time,
				count=200,
				minute=minute,
				client=client
			)
			print("현재시각 : ", current_time)
			current_time = current_time + 60 * ohlc_jsons.__len__()
			sql_set = set()
			sql_set, _ = self.upbit_parse_ohlc(ohlc_jsons, sql_set, market_pair, 0)
			sql_query_set = sql_query_set.union(sql_set)

		return {"data" : sql_query_set, "table_name" : candle_cls.__tablename__, "updated_or_not" : True, "market_info" : first_candle}

	async def async_upbit_ohlc_commit(self, sql_set, table_name):
		sql_str = repr(sql_set)[1:-1]
		sql = "INSERT INTO %s (time_stamp, crypto_exchange, crypto_pair, open_price, high_price, low_price, close_price, volume, money_flow) " \
		"VALUES %s " \
		"ON DUPLICATE KEY UPDATE " \
		"open_price=VALUES(open_price), high_price=VALUES(high_price), low_price=VALUES(low_price), close_price=VALUES(close_price), volume=VALUES(volume), money_flow=VALUES(money_flow);" \
		% (table_name, sql_str)
		self.upbit_collector.logger.info(f'market_pair : {next(iter(sql_set))[2]}\ninserted data : {len(sql_str)}\n')
		self.upbit_collector.db_session.execute(sql)
		self.upbit_collector.db_session.commit()
			# except:
			# 	self.upbit_collector.logger.error(f"sql : \n{sql}\ntable_name : {table_name}")
			# 	sleep(10)

	"""
	return 형식이 달라졌다.
	{"code":"CRIX.UPBIT.KRW-DCR",
	"candleDateTime":"2018-07-26T11:16:00+00:00",
	"candleDateTimeKst":"2018-07-26T20:16:00+09:00",
	"openingPrice":73600.00000000,
	"highPrice":73600.00000000,
	"lowPrice":73600.00000000,
	"tradePrice":73600.00000000,
	"candleAccTradeVolume":0.48478324,
	"candleAccTradePrice":35680.04646400,
	"timestamp":1532603769155,
	"unit":1
	"""
	def upbit_parse_ohlc(self, ohlc_jsons, sql_set, market_pair, lowest_timestamp):
		tmp_timestamp = lowest_timestamp

		for ohlc in ohlc_jsons:
			current_timestamp = self.upbit_collector.convert_iso_to_timestamp(ohlc["candleDateTimeKst"])
			if tmp_timestamp > current_timestamp:
				tmp_timestamp = current_timestamp
			sql_set.add(
				(current_timestamp,
				 market_pair.crypto_exchange, 
				 market_pair.crypto_pair,
				 ohlc["openingPrice"],
				 ohlc["highPrice"],
				 ohlc["lowPrice"],
				 ohlc["tradePrice"],
				 ohlc["candleAccTradeVolume"],
				 ohlc["candleAccTradePrice"]
				 )
			)
		return sql_set, tmp_timestamp

	def upbit_ohlc_commit(self, table_name, sql_set):
		sql_str = repr(sql_set)[1:-1]
		sql = "INSERT INTO %s (time_stamp, crypto_exchange, crypto_pair, open_price, high_price, low_price, close_price, volume, money_flow) " \
			  "VALUES %s " \
			  "ON DUPLICATE KEY UPDATE " \
			  "open_price=VALUES(open_price), high_price=VALUES(high_price), low_price=VALUES(low_price), close_price=VALUES(close_price), volume=VALUES(volume), money_flow=VALUES(money_flow);" \
			  % (table_name, sql_str)
		self.upbit_collector.db_session.execute(sql)
		self.upbit_collector.db_session.commit()

	def cryptoWatch_collect_ohlc(self):
		market_pairs = CryptoMarket.query.filter_by(crypto_exchange='bithumb').all()
		# print(market_pairs)
		candle_list = [Candle3M, Candle5M, Candle15M, Candle30M, Candle1H, Candle2H,
					   Candle4H, Candle6H, Candle12H, Candle1D, Candle3D, Candle1W, Candle1M]

		# 한번에 6000개 가져옴

		# candle_list = [Candle1M, ]
		count = 0

		for candle_cls in candle_list:
			print("***", candle_cls.__name__, "를 시작합니다.")
			for market_pair in market_pairs:
				print("**", market_pair, "를 시작합니다.")
				# 데이터 변경하자 한번에 200개 가져옴 [Upbit기준]]
				# 업비트는 데이터를 crypto랑 다르게 줌..
				while True:
					count += 1
					last_candle = candle_cls.query.filter_by(
						crypto_exchange=market_pair.crypto_exchange, crypto_pair=market_pair.crypto_pair
					).order_by(candle_cls.time_stamp.desc()).first()  # 내림차순으로 가져옴

					if not last_candle:
						start_timestamp = 1

					else:
						start_timestamp = last_candle.time_stamp + 1

					# 1530559020
					ohlc_json = self.crypto_collector.get_ohlc(market_pair.crypto_exchange, market_pair.crypto_pair,
															   after=str(start_timestamp),
															   periods=str(candle_cls._seconds))
					allowance = ohlc_json.get('allowance', None)
					if not allowance:
						continue
					if allowance['remaining'] < 2000000:
						time.sleep(900)

					ohlc_result = ohlc_json.get('result', None)
					if not ohlc_result:
						# 끝까지 다 돈 것
						print("들어왓다")
						break
					if not ohlc_result[str(candle_cls._seconds)]:
						print("들어왓다")
						break

					if ohlc_result[str(candle_cls._seconds)][0][0] < start_timestamp:
						print("들어왓다")
						break

					print(count, "요청중,", start_timestamp, " 시간부터",
						  "%s - %s" % (market_pair.crypto_pair, market_pair.crypto_exchange))

					ohlc_result = ohlc_result[str(candle_cls._seconds)]  # 맞는 초를 가져옴
					print(len(ohlc_result))
					sql_set = set()
					for ohlc in ohlc_result:
						sql_set.add(
							(ohlc[0], market_pair.crypto_exchange, market_pair.crypto_pair, ohlc[1], ohlc[2], ohlc[3],
							 ohlc[4], ohlc[5], ohlc[6])
						)
					sql_str = repr(sql_set)[1:-1]

					sql = "INSERT INTO %s (time_stamp, crypto_exchange, crypto_pair, open_price, high_price, low_price, close_price, volume, money_flow) " \
						  "VALUES %s " \
						  "ON DUPLICATE KEY UPDATE " \
						  "open_price=VALUES(open_price), high_price=VALUES(high_price), low_price=VALUES(low_price), close_price=VALUES(close_price), volume=VALUES(volume), money_flow=VALUES(money_flow);" \
						  % (candle_cls.__tablename__, sql_str)

					self.crypto_collector.db_session.execute(sql)
					self.crypto_collector.db_session.commit()

	def collect_all_ohlc(self):
		self.cryptoWatch_collect_ohlc()

	def initial_ohlc(self):
		# self.crypto_collector.get_ohlc()
		pass

	def run(self):
		self.collect_all_ohlc()
		pass
	
if __name__ == "__main__":
	logger_class = CrawlerLogger()
	collector = Collector()
	current_time = time.time()
	# collector.upbit_collect_crypto_pair()
	loop = asyncio.get_event_loop()

	# loop.run_until_complete(collector.upbit_collector._web_socket_get_tick())

	client = aiohttp.ClientSession(loop=loop)
	loop.run_until_complete(collector.async_upbit_collect_historical_ohlc(client))
	client = aiohttp.ClientSession(loop=loop)
	loop.run_until_complete(collector.async_upbit_collect_current_ohlc(client))
	running_time = time.time() - current_time
	logger_class._logger.info(f"request 요청완료 \n running time : {running_time} ")
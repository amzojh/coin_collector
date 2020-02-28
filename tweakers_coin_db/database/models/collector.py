from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relationship

try:
	from database import Base
except:
	from tweakers_coin_db.database import Base


class Exchanges(Base):  # from Exchanges to Currency (one to many)
	__tablename__ = "exchanges"
	#     exchange_id = Column(Integer, autoincrement=True, unique_key=True)
	exchange_name = Column(String(30), nullable=False)
	exchange_symbol = Column(String(30), primary_key=True)
	CryptoMarket = relationship("CryptoMarket", back_populates="Exchanges")
	Candle1M = relationship("Candle1M", back_populates="Exchanges")
	Candle3M = relationship("Candle3M", back_populates="Exchanges")
	Candle5M = relationship("Candle5M", back_populates="Exchanges")
	Candle15M = relationship("Candle15M", back_populates="Exchanges")
	Candle30M = relationship("Candle30M", back_populates="Exchanges")
	Candle1H = relationship("Candle1H", back_populates="Exchanges")
	Candle2H = relationship("Candle2H", back_populates="Exchanges")
	Candle4H = relationship("Candle4H", back_populates="Exchanges")
	Candle6H = relationship("Candle6H", back_populates="Exchanges")
	Candle12H = relationship("Candle12H", back_populates="Exchanges")
	Candle1D = relationship("Candle1D", back_populates="Exchanges")
	Candle3D = relationship("Candle3D", back_populates="Exchanges")
	Candle1W = relationship("Candle1W", back_populates="Exchanges")
	Candle4W = relationship('Candle4W', back_populates="Exchanges")

	def __repr__(self):
		return "<Exchange(exchange_name='%s',exchange_symbol='%s')" % (
			self.exchange_name, self.exchange_symbol)

class Upbit(Base):
	__tablename__ = "upbit_pair"
	original_symbol = Column(String(40), nullable=False)
	symbol = Column(String(40), ForeignKey('cryptomarket.crypto_pair'), primary_key=True)

class Currency(Base):
	__tablename__ = "currency"
	#     currency_id = Column(Integer, nullable=False)
	currency_name = Column(String(50), nullable=False)
	currency_symbol = Column(String(50), primary_key=True)
	is_fiat = Column(Boolean, nullable=False)

	#     BaseCryptoMarket = relationship("CryptoMarket", back_populates="BaseCurrency")
	#     QuoteCryptoMarket = relationship("CryptoMarket", back_populates="QuoteCurrency")

	def __repr__(self):
		return "<Currency(currency_name='%s', currency_symbol='%s', is_fiat='%s')>" % (
			self.currency_name, self.currency_symbol, self.is_fiat)


class CryptoPair(Base):
	__tablename__ = 'cryptopair'
	base_currency = Column(String(50), ForeignKey("currency.currency_symbol"), primary_key=True)
	quote_currency = Column(String(50), ForeignKey("currency.currency_symbol"), primary_key=True)

	BaseCurrency = relationship("Currency", foreign_keys=[base_currency])
	QuoteCurrency = relationship("Currency", foreign_keys=[quote_currency])

class CryptoMarket(Base):
	__tablename__ = "cryptomarket"
	#     crypto_id = Column(Integer)
	crypto_pair = Column(String(40), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)  # foreign key
	update_completed = Column(String(1), nullable=False, default='N') # N 인경우 업데이트 아닌경우 Y
	api_src = Column(String(30))

	# Foreign key 관리는 Exchanges
	Exchanges = relationship("Exchanges", back_populates="CryptoMarket")

	#     Candle1M = relationship("Candle1M", back_populates="CryptoMarket")
	#     Candle3M = relationship("Candle3M", back_populates="CryptoMarket")
	#     Candle15M = relationship("Candle15M", back_populates="CryptoMarket")
	#     Candle30M = relationship("Candle30M", back_populates="CryptoMarket")
	#     Candle1H = relationship("Candle1H", back_populates="CryptoMarket")
	#     Candle2H = relationship("Candle2H", back_populates="CryptoMarket")
	#     Candle3H = relationship("Candle3H", back_populates="CryptoMarket")
	#     Candle6H = relationship("Candle6H", back_populates="CryptoMarket")
	#     Candle12H = relationship("Candle12H", back_populates="CryptoMarket")
	#     Candle1D = relationship("Candle1D", back_populates="CryptoMarket")
	#     Candle3D = relationship("Candle3D", back_populates="CryptoMarket")
	#     Candle1W = relationship("Candle1W", back_populates="CryptoMarket")

	def __repr__(self):
		return "<CryptoPair(crypto_pair='%s', crypto_exchange='%s')" % (
			self.crypto_pair, self.crypto_exchange)

#  Base candle에서 _seconds와 _type, Exchanges에서의 relationshop을 재정의

class BaseCandle(Base):
	__abstract__ = True
	open_price = Column(Float, nullable=False)
	high_price = Column(Float, nullable=False)
	low_price = Column(Float, nullable=False)
	close_price = Column(Float, nullable=False)
	volume = Column(Float, nullable=False)
	money_flow = Column(Float)


class Candle1M(BaseCandle):
	__tablename__ = "candle1m"
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	Exchanges = relationship("Exchanges", back_populates="Candle1M")
	_seconds = 60
	_type = "min"
	def __repr__(self):
		return "<Candle1M(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle3M(BaseCandle):
	__tablename__ = "candle3m"
	Exchanges = relationship("Exchanges", back_populates="Candle3M")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_seconds = 180
	_type = "min"

	def __repr__(self):
		return "<Candle3M(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle5M(BaseCandle):
	__tablename__ = "candle5m"
	Exchanges = relationship("Exchanges", back_populates="Candle5M")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "min"
	_seconds = 300
	def __repr__(self):
		return "<Candle5M(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle15M(BaseCandle):
	__tablename__ = "candle15m"
	Exchanges = relationship("Exchanges", back_populates="Candle15M")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "min"
	_seconds = 900
	def __repr__(self):
		return "<Candle15M(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle30M(BaseCandle):
	__tablename__ = "candle30m"
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])

	# Foreign Key관리
	Exchanges = relationship("Exchanges", back_populates="Candle30M")
	#     CryptoMarketID = relationship("CryptoMarket", foreign_keys=[crypto_id])
	_type = "min"

	_seconds = 1800
	def __repr__(self):
		return "<Candle30M(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle1H(BaseCandle):
	__tablename__ = "candle1h"

	Exchanges = relationship("Exchanges", back_populates="Candle1H")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "hour"
	_seconds = 3600

	def __repr__(self):
		return "<Candle1H(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle2H(BaseCandle):
	__tablename__ = "candle2h"
	Exchanges = relationship("Exchanges", back_populates="Candle2H")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "hour"
	_seconds = 7200
	def __repr__(self):
		return "<Candle2H(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle4H(BaseCandle):
	__tablename__ = "candle4h"

	# Foreign Key관리
	Exchanges = relationship("Exchanges", back_populates="Candle4H")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "hour"
	_seconds = 14400
	def __repr__(self):
		return "<Candle4H(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle6H(BaseCandle):
	__tablename__ = "candle6h"
	# Foreign Key관리
	Exchanges = relationship("Exchanges", back_populates="Candle6H")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])

	#     CryptoMarketID = relationship("CryptoMarket", foreign_keys=[crypto_id])
	_type = "hour"
	_seconds = 21600
	def __repr__(self):
		return "<Candle6H(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle12H(BaseCandle):
	__tablename__ = "candle12h"
	Exchanges = relationship("Exchanges", back_populates="Candle12H")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "hour"
	_seconds = 43200
	def __repr__(self):
		return "<Candle12H(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle1D(BaseCandle):
	__tablename__ = "candle1d"
	Exchanges = relationship("Exchanges", back_populates="Candle1D")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "day"
	_seconds = 86400

	def __repr__(self):
		return "<Candle1D(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle3D(BaseCandle):
	__tablename__ = "candle3d"

	# Foreign Key관리
	Exchanges = relationship("Exchanges", back_populates="Candle3D")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "min"
	_seconds = 259200
	def __repr__(self):
		return "<Candle3D(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle1W(BaseCandle):
	__tablename__ = "candle1w"
	Exchanges = relationship("Exchanges", back_populates="Candle1W")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	_type = "week"
	_seconds = 604800
	def __repr__(self):
		return "<Candle1W(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)


class Candle4W(BaseCandle):
	__tablename__ = "candle4w"
	Exchanges = relationship("Exchanges", back_populates="Candle4W")
	time_stamp = Column(Integer(), primary_key=True)
	crypto_exchange = Column(String(30), ForeignKey("exchanges.exchange_symbol"), primary_key=True)
	crypto_pair = Column(String(40), ForeignKey("cryptomarket.crypto_pair"), primary_key=True)
	CryptoMarketPair = relationship("CryptoMarket", foreign_keys=[crypto_pair])
	#     CryptoMarketID = relationship("CryptoMarket", foreign_keys=[crypto_id])
	_type = "month"
	_seconds = 604800 * 4
	def __repr__(self):
		return "<Candle4W(time_stamp='%s' crypto_exchange ='%s' crypto_pair ='%s' open_price='%s' high_price='%s' low_price='%s' close_price='%s' volume='%s' money_flow = '%s')" % (
			self.time_stamp, self.crypto_exchange, self.crypto_pair, self.open_price, self.high_price,
			self.low_price, self.close_price, self.volume, self.money_flow)

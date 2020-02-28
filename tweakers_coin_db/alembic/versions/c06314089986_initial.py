"""initial

Revision ID: c06314089986
Revises: 
Create Date: 2018-06-26 21:26:03.278221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c06314089986'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('currency_name', sa.String(length=50), nullable=False),
    sa.Column('currency_symbol', sa.String(length=50), nullable=False),
    sa.Column('is_fiat', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('currency_symbol')
    )
    op.create_table('exchanges',
    sa.Column('exchange_name', sa.String(length=30), nullable=False),
    sa.Column('exchange_symbol', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('exchange_symbol')
    )
    op.create_table('cryptomarket',
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('base_currency', sa.String(length=50), nullable=True),
    sa.Column('quote_currency', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['base_currency'], ['currency.currency_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['quote_currency'], ['currency.currency_symbol'], ),
    sa.PrimaryKeyConstraint('crypto_pair', 'crypto_exchange')
    )
    op.create_table('candle12h',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle15m',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=15), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle1d',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle1h',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle1m',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle1w',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle2h',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle30m',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle3d',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle3m',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle4h',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle5m',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    op.create_table('candle6h',
    sa.Column('time_stamp', sa.Integer(), nullable=False),
    sa.Column('crypto_exchange', sa.String(length=30), nullable=False),
    sa.Column('crypto_pair', sa.String(length=40), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('money_flow', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
    sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candle6h')
    op.drop_table('candle5m')
    op.drop_table('candle4h')
    op.drop_table('candle3m')
    op.drop_table('candle3d')
    op.drop_table('candle30m')
    op.drop_table('candle2h')
    op.drop_table('candle1w')
    op.drop_table('candle1m')
    op.drop_table('candle1h')
    op.drop_table('candle1d')
    op.drop_table('candle15m')
    op.drop_table('candle12h')
    op.drop_table('cryptomarket')
    op.drop_table('exchanges')
    op.drop_table('currency')
    # ### end Alembic commands ###

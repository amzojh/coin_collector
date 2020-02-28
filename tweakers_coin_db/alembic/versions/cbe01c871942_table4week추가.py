"""테이블 추가

Revision ID: cbe01c871942
Revises: 981550529073
Create Date: 2018-07-23 09:15:00.943013

"""
from alembic import op
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column, ForeignKey, Float
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbe01c871942'
down_revision = '981550529073'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'candle4w',
        Column('time_stamp', INTEGER),
        Column('crypto_exchange', VARCHAR(30), ForeignKey("exchanges.exchange_symbol")),
        Column('crypto_pair', VARCHAR(40), ForeignKey("cryptomarket.crypto_pair")),
        Column('open_price', Float, nullable=False),
        Column('higd_price', Float, nullable=False),
        Column('low_price', Float, nullable=False),
        Column('close_price', Float, nullable=False),
        Column('volume', Float, nullable=False),
        Column('money_flow', Float),
        sa.PrimaryKeyConstraint('time_stamp', 'crypto_exchange', 'crypto_pair'),
        sa.ForeignKeyConstraint(['crypto_exchange'], ['exchanges.exchange_symbol'], ),
        sa.ForeignKeyConstraint(['crypto_pair'], ['cryptomarket.crypto_pair'], ),
    )

    op.create_table(
        'upbit_pair',
        Column('original_symbol', VARCHAR(40), nullable=False),
        Column('symbol', VARCHAR(40)),
        sa.PrimaryKeyConstraint('symbol'),
        sa.ForeignKeyConstraint(['symbol'], ['cryptomarket.crypto_pair'],)
    )
    pass


def downgrade():
    op.drop_table('candle4w')
    op.drop_table('upbit_pair')
    pass

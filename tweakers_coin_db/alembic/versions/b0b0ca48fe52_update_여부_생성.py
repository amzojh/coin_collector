"""update 여부 생성

Revision ID: b0b0ca48fe52
Revises: cbe01c871942
Create Date: 2019-01-04 21:44:05.151552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0b0ca48fe52'
down_revision = 'cbe01c871942'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('cryptomarket', sa.Column('update_completed', sa.String(length=1), nullable=False, default='N'))
    pass


def downgrade():
    op.drop_column('cryptomarket', 'update_completed')
    pass

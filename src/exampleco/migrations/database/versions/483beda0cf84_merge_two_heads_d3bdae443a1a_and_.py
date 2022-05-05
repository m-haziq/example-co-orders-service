"""merge two heads d3bdae443a1a and 52ad861d3c4c

Revision ID: 483beda0cf84
Revises: d3bdae443a1a, 52ad861d3c4c
Create Date: 2022-04-28 13:37:42.510251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483beda0cf84'
down_revision = ('d3bdae443a1a', '52ad861d3c4c')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

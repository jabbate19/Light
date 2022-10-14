"""Whitelist and Lock for Rooms

Revision ID: 791ecb5ce933
Revises: b5880584b3d0
Create Date: 2022-01-18 22:09:46.209242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '791ecb5ce933'
down_revision = 'b5880584b3d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('room', sa.Column('whitelist', sa.String(255), nullable=True))
    op.add_column('room', sa.Column('lock', sa.Boolean, nullable=False))


def downgrade():
    op.drop_column('room', 'whitelist')
    op.drop_column('room', 'lock')


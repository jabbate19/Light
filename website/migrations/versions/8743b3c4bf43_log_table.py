"""Log Table

Revision ID: 8743b3c4bf43
Revises: 8f68f173234c
Create Date: 2021-11-12 15:55:54.095075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8743b3c4bf43'
down_revision = '8f68f173234c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('logs',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column('user',sa.String(50), nullable=False),
        sa.Column('timestamp',sa.String(50), nullable=False),
        sa.Column('device',sa.String(50), nullable=False),
        sa.Column('style', sa.String(50), nullable=False),
        sa.Column('color1', sa.String(50), nullable=False),
        sa.Column('color2', sa.String(50), nullable=False),
        sa.Column('color3', sa.String(50), nullable=False)
    )


def downgrade():
    op.drop_table('logs')

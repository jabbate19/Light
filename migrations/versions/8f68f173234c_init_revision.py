"""Init Revision

Revision ID: 8f68f173234c
Revises: 
Create Date: 2021-11-10 16:24:27.105082

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.sql.expression import null

# revision identifiers, used by Alembic.
revision = '8f68f173234c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('firstname', sa.String(50), nullable=False),
        sa.Column('lastname', sa.String(50), nullable=False),
        sa.Column('picture', sa.String(255), nullable=False)
    )
    op.create_table('room',
        sa.Column('id', sa.String(50), primary_key=True, nullable=False),
        sa.Column('mac', sa.String(50), nullable=False),
        sa.Column('style', sa.String(50), nullable=False),
        sa.Column('color1', sa.String(50), nullable=False),
        sa.Column('color2', sa.String(50), nullable=False),
        sa.Column('color3', sa.String(50), nullable=False),
        sa.Column('last_modify_user', sa.String(50), nullable=False),
        sa.Column('last_modify_time', sa.String(50), nullable=False),
        sa.Column('session_id', sa.String(50), nullable=True)
    )


def downgrade():
    op.drop_table('room')

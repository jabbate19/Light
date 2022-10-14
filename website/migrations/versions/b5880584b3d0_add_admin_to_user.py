"""Add admin to user

Revision ID: b5880584b3d0
Revises: 8743b3c4bf43
Create Date: 2022-01-18 01:25:51.403396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5880584b3d0'
down_revision = '8743b3c4bf43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('admin', sa.Boolean, nullable=False))


def downgrade():
    op.drop_column('user','admin')


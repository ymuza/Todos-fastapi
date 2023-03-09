"""add apartment number column

Revision ID: 87c7e83d00b0
Revises: a40dda76cbfe
Create Date: 2023-03-09 11:59:02.705869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c7e83d00b0'
down_revision = 'a40dda76cbfe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apartment_number', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apartment_number')

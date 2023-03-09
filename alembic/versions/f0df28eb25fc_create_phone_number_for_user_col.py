"""create phone number for user col

Revision ID: f0df28eb25fc
Revises: 
Create Date: 2023-03-08 12:14:26.460708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0df28eb25fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """upgrades the database by adding, removing or modifying columns"""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')



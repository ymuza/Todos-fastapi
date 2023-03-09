"""create address table

Revision ID: 6e832f9e17af
Revises: f0df28eb25fc
Create Date: 2023-03-08 12:33:03.002576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e832f9e17af'
down_revision = 'f0df28eb25fc'  # this is the last revision
branch_labels = None
depends_on = None


def upgrade() -> None:
    """upgrades the database by adding, removing or modifying columns"""
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postalcode', sa.String(), nullable=False),
                    )

    pass


def downgrade() -> None:
    op.drop_table('address')  # if we want to delete the upgrade

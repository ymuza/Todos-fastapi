"""create address_id to users

Revision ID: a40dda76cbfe
Revises: 6e832f9e17af
Create Date: 2023-03-08 12:40:52.109199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a40dda76cbfe'
down_revision = '6e832f9e17af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table="users", referent_table="address",
                          local_cols=['address_id'], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name="users")
    op.drop_column('users', 'address_id')

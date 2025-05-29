"""add_name_field_to_users_table

Revision ID: 4d1c657fd3a1
Revises: 2df073c7b564
Create Date: 2025-05-28 23:19:27.521398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d1c657fd3a1'
down_revision: Union[str, None] = '2df073c7b564'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add name column to users table
    op.add_column('users', sa.Column('name', sa.String(), nullable=False, server_default=''))
    # Remove server_default after adding the column
    op.alter_column('users', 'name', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove name column from users table
    op.drop_column('users', 'name')

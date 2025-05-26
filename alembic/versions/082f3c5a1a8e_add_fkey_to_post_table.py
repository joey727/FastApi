"""add fkey to post table

Revision ID: 082f3c5a1a8e
Revises: ece75b3c2401
Create Date: 2025-05-26 16:26:33.462307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '082f3c5a1a8e'
down_revision: Union[str, None] = 'ece75b3c2401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fkey', source_table='posts',
                          referent_table='users', local_cols=['owner_id'], remote_cols=['user_id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')

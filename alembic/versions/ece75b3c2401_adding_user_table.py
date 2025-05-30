"""adding user table

Revision ID: ece75b3c2401
Revises: a208d3230336
Create Date: 2025-05-26 16:01:04.100476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ece75b3c2401'
down_revision: Union[str, None] = 'a208d3230336'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', sa.Column(
        'user_id', sa.Integer, nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass

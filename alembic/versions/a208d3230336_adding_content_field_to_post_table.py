"""adding content field to post table

Revision ID: a208d3230336
Revises: ced9caa3c9b4
Create Date: 2025-05-26 15:47:16.861489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a208d3230336'
down_revision: Union[str, None] = 'ced9caa3c9b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')

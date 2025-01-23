"""add content column to posts table

Revision ID: 9578a762018a
Revises: 3c7d51397078
Create Date: 2025-01-18 17:56:09.337583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9578a762018a'
down_revision: Union[str, None] = '3c7d51397078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

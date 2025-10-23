"""init tables

Revision ID: ce61568655fd
Revises: 06cef3402811
Create Date: 2025-10-23 17:08:26.342389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce61568655fd'
down_revision: Union[str, Sequence[str], None] = '06cef3402811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

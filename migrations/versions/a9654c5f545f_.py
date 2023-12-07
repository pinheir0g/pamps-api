"""empty message

Revision ID: a9654c5f545f
Revises: d451b4200786
Create Date: 2023-12-05 13:30:09.097301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a9654c5f545f'
down_revision: Union[str, None] = 'd451b4200786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

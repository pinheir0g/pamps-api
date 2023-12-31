"""initial

Revision ID: 6cd081153def
Revises: 
Create Date: 2023-12-05 13:19:01.909894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6cd081153def'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('avatar', sa.String()),
    sa.Column('bio', sa.String()),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String()),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer()),
    sa.Column('parent_id', sa.Integer()),
    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    sa.ForeignKeyConstraint(['parent_id'], ['post.id']),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
    

def downgrade() -> None:
    pass
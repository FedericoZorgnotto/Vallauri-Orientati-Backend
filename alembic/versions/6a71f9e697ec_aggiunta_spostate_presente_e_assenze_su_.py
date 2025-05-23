"""Aggiunta spostate presente e assenze su ragazzo

Revision ID: 6a71f9e697ec
Revises: 537921d9f3ad
Create Date: 2025-03-01 20:29:39.655696

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6a71f9e697ec'
down_revision: Union[str, None] = '537921d9f3ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Assenti',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('ragazzo_id', sa.Integer(), nullable=False),
                    sa.Column('gruppo_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['gruppo_id'], ['Gruppi.id'], ),
                    sa.ForeignKeyConstraint(['ragazzo_id'], ['Ragazzi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Presenti',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('ragazzo_id', sa.Integer(), nullable=False),
                    sa.Column('gruppo_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['gruppo_id'], ['Gruppi.id'], ),
                    sa.ForeignKeyConstraint(['ragazzo_id'], ['Ragazzi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Presenti')
    op.drop_table('Assenti')
    # ### end Alembic commands ###

"""gestione utenti temporanei

Revision ID: 288b9f8c8850
Revises: 78c60cfd8dc6
Create Date: 2024-10-21 09:20:29.208729

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '288b9f8c8850'
down_revision: Union[str, None] = '78c60cfd8dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('utenti',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('admin', sa.Boolean(), nullable=False),
                    sa.Column('temporaneo', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_utenti_nome'), 'utenti', ['nome'], unique=True)
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('username', sa.VARCHAR(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=True),
                    sa.Column('surname', sa.VARCHAR(), nullable=True),
                    sa.Column('email', sa.VARCHAR(), nullable=False),
                    sa.Column('hashed_password', sa.VARCHAR(), nullable=False),
                    sa.Column('is_admin', sa.BOOLEAN(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_users_username', 'users', ['username'], unique=1)
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    op.drop_index(op.f('ix_utenti_nome'), table_name='utenti')
    op.drop_table('utenti')
    # ### end Alembic commands ###

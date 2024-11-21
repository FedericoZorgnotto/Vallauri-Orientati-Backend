"""id utente in log opzionale

Revision ID: 82d2f7cc72dc
Revises: dd11de38f4cf
Create Date: 2024-11-17 01:30:08.500898

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '82d2f7cc72dc'
down_revision: Union[str, None] = 'dd11de38f4cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_action_logs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('utente_id', sa.Integer(), nullable=True),
                    sa.Column('categoria', sa.Enum('INFO', 'WARNING', 'ERROR', 'CRITICAL', name='categorialogutente'),
                              nullable=False),
                    sa.Column('azione', sa.String(length=255), nullable=False),
                    sa.Column('dati', sa.JSON(), nullable=True),
                    sa.Column('orario', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['utente_id'], ['Utenti.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_user_action_logs_id'), 'user_action_logs', ['id'], unique=False)
    op.create_index(op.f('ix_user_action_logs_utente_id'), 'user_action_logs', ['utente_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_action_logs_utente_id'), table_name='user_action_logs')
    op.drop_index(op.f('ix_user_action_logs_id'), table_name='user_action_logs')
    op.drop_table('user_action_logs')
    # ### end Alembic commands ###

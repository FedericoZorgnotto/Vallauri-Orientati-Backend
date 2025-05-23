"""rimosso orientatore

Revision ID: 7306b1fdc787
Revises: 13c22af60bc4
Create Date: 2024-11-24 21:53:01.551893

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7306b1fdc787'
down_revision: Union[str, None] = '13c22af60bc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Utenti', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gruppo_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_utenti_orientatore_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_utenti_gruppo_id', 'Gruppi', ['gruppo_id'], ['id'])
        batch_op.drop_column('orientatore_id')

    with op.batch_alter_table('Gruppi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('codice', sa.String(length=255), nullable=True))

    op.drop_table('Association_orientatori_gruppi')
    op.drop_table('Orientatori')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Orientatori',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('nome', sa.VARCHAR(), nullable=False),
                    sa.Column('cognome', sa.VARCHAR(), nullable=False),
                    sa.Column('classe', sa.VARCHAR(), nullable=False),
                    sa.Column('email', sa.VARCHAR(), nullable=False),
                    sa.Column('indirizzo_id', sa.INTEGER(), nullable=False),
                    sa.Column('codice', sa.VARCHAR(), nullable=True),
                    sa.ForeignKeyConstraint(['indirizzo_id'], ['Indirizzi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('Association_orientatori_gruppi',
                    sa.Column('idOrientatore', sa.INTEGER(), nullable=True),
                    sa.Column('idGruppo', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['idGruppo'], ['Gruppi.id'], ),
                    sa.ForeignKeyConstraint(['idOrientatore'], ['Orientatori.id'], )
                    )

    with op.batch_alter_table('Utenti', schema=None) as batch_op:
        batch_op.add_column(sa.Column('orientatore_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint('fk_utenti_gruppo_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_utenti_orientatore_id', 'Orientatori', ['orientatore_id'], ['id'])
        batch_op.drop_column('gruppo_id')

    with op.batch_alter_table('Gruppi', schema=None) as batch_op:
        batch_op.drop_column('codice')
    # ### end Alembic commands ###

"""aggiunte tabelle

Revision ID: 2b8a208e2316
Revises: 
Create Date: 2024-10-28 20:53:09.615521

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2b8a208e2316'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Aule',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('posizione', sa.String(), nullable=False),
                    sa.Column('materia', sa.String(), nullable=False),
                    sa.Column('dettagli', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('PercorsiDiStudi',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('ScuoleDiProvenienza',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('citta', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Utenti',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('admin', sa.Boolean(), nullable=False),
                    sa.Column('temporaneo', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_Utenti_username'), 'Utenti', ['username'], unique=True)
    op.create_table('Indirizzi',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('percorsoDiStudi_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['percorsoDiStudi_id'], ['PercorsiDiStudi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Orientati',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('cognome', sa.String(), nullable=False),
                    sa.Column('classe', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('scuolaDiProvenienza_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['scuolaDiProvenienza_id'], ['ScuoleDiProvenienza.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Percorsi',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('percorsoDiStudi_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['percorsoDiStudi_id'], ['PercorsiDiStudi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Gruppi',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('data', sa.String(), nullable=False),
                    sa.Column('percorso_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['percorso_id'], ['Percorsi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Orientatori',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('nome', sa.String(), nullable=False),
                    sa.Column('cognome', sa.String(), nullable=False),
                    sa.Column('indirizzo_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['indirizzo_id'], ['Indirizzi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Tappe',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('percorso_id', sa.Integer(), nullable=False),
                    sa.Column('aula_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['aula_id'], ['Aule.id'], ),
                    sa.ForeignKeyConstraint(['percorso_id'], ['Percorsi.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Association_orientati_gruppi',
                    sa.Column('idOrientato', sa.Integer(), nullable=True),
                    sa.Column('idGruppo', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['idGruppo'], ['Gruppi.id'], ),
                    sa.ForeignKeyConstraint(['idOrientato'], ['Orientati.id'], )
                    )
    op.create_table('Association_orientatori_gruppi',
                    sa.Column('idOrientatore', sa.Integer(), nullable=True),
                    sa.Column('idGruppo', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['idGruppo'], ['Gruppi.id'], ),
                    sa.ForeignKeyConstraint(['idOrientatore'], ['Orientatori.id'], )
                    )

    op.execute(
        """
        INSERT INTO utenti (username, hashed_password, admin, temporaneo)
        VALUES ('admin', '$2b$12$Fyp.CIuqwcrqs09Oklz71eVMcwHBTP11x3FBj.B6LiUl7dxEYuaO2', true, false)
        """
    )  # password: admin

    op.execute(
        """
        INSERT INTO utenti (username, hashed_password, admin, temporaneo)
        VALUES ('user', '$2b$12$KYaTyisWLNtSnGOoo1B.3ue7oN/6abk0BeZupZX1BVKNf.JsTQrlW', false, false) 
        """
    )  # password: user

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Association_orientatori_gruppi')
    op.drop_table('Association_orientati_gruppi')
    op.drop_table('Tappe')
    op.drop_table('Orientatori')
    op.drop_table('Gruppi')
    op.drop_table('Percorsi')
    op.drop_table('Orientati')
    op.drop_table('Indirizzi')
    op.drop_index(op.f('ix_Utenti_username'), table_name='Utenti')
    op.drop_table('Utenti')
    op.drop_table('ScuoleDiProvenienza')
    op.drop_table('PercorsiDiStudi')
    op.drop_table('Aule')
    # ### end Alembic commands ###

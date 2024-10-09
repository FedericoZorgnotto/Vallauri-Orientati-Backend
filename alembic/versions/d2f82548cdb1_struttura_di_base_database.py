"""struttura di base database

Revision ID: d2f82548cdb1
Revises: 
Create Date: 2024-10-10 08:36:14.481387

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd2f82548cdb1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_routes_name'), 'routes', ['name'], unique=True)
    op.create_table('specialisations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_specialisations_name'), 'specialisations', ['name'], unique=True)
    op.create_table('groups',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('start_hour', sa.String(), nullable=False),
                    sa.Column('notes', sa.String(), nullable=False),
                    sa.Column('route_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('args', sa.String(), nullable=False),
                    sa.Column('specialisation_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['specialisation_id'], ['specialisations.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_rooms_name'), 'rooms', ['name'], unique=True)
    op.create_table('stages',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('start_minute', sa.Integer(), nullable=False),
                    sa.Column('end_minute', sa.Integer(), nullable=False),
                    sa.Column('route_id', sa.Integer(), nullable=False),
                    sa.Column('room_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
                    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('surname', sa.String(), nullable=True),
                    sa.Column('year', sa.Integer(), nullable=True),
                    sa.Column('section', sa.String(), nullable=True),
                    sa.Column('specialisation_id', sa.Integer(), nullable=True),
                    sa.Column('group_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
                    sa.ForeignKeyConstraint(['specialisation_id'], ['specialisations.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # aggiungo i dati di base

    op.execute("INSERT INTO specialisations (name) VALUES ('Informatica')")
    op.execute("INSERT INTO specialisations (name) VALUES ('Elettrotecnica')")
    op.execute("INSERT INTO specialisations (name) VALUES ('Meccanica')")
    op.execute("INSERT INTO specialisations (name) VALUES ('Liceo')")

    op.execute(
        """
        INSERT INTO users (username, email, hashed_password, is_admin, name, surname, year, section, specialisation_id)
        VALUES ('admin', 'admin@admin.com', '$2b$12$Fyp.CIuqwcrqs09Oklz71eVMcwHBTP11x3FBj.B6LiUl7dxEYuaO2', true, 'Admin', 'Admin', null, null, null)
        """
    )  # password: admin

    op.execute(
        """
        INSERT INTO users (username, email, hashed_password, is_admin, name, surname, year, section, specialisation_id)
        VALUES ('user', 'user@user.com', '$2b$12$KYaTyisWLNtSnGOoo1B.3ue7oN/6abk0BeZupZX1BVKNf.JsTQrlW', False, 'User', 'User', 1, 'A', 1) 
        """
    )  # password: user

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('stages')
    op.drop_index(op.f('ix_rooms_name'), table_name='rooms')
    op.drop_table('rooms')
    op.drop_table('groups')
    op.drop_index(op.f('ix_specialisations_name'), table_name='specialisations')
    op.drop_table('specialisations')
    op.drop_index(op.f('ix_routes_name'), table_name='routes')
    op.drop_table('routes')
    # ### end Alembic commands ###

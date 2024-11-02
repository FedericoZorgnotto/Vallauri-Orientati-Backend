"""aggiunti minuti tappa

Revision ID: ca439a6160f6
Revises: 02c63fa39091
Create Date: 2024-11-02 11:57:19.817381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca439a6160f6'
down_revision: Union[str, None] = '02c63fa39091'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tappe', sa.Column('minuti_arrivo', sa.Integer(), nullable=False))
    op.add_column('Tappe', sa.Column('minuti_partenza', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Tappe', 'minuti_partenza')
    op.drop_column('Tappe', 'minuti_arrivo')
    # ### end Alembic commands ###

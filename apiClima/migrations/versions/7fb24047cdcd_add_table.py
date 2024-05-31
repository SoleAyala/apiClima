"""Add table

Revision ID: 7fb24047cdcd
Revises: cbfdecae6f07
Create Date: 2024-05-27 22:54:56.669324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fb24047cdcd'
down_revision = 'cbfdecae6f07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('precipitacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.Column('cantidad', sa.Float(), nullable=False),
    sa.Column('unidad', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('precipitacion')
    # ### end Alembic commands ###
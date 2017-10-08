"""initial migration

Revision ID: 82213d98918c
Revises: 
Create Date: 2017-10-08 03:06:06.594726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82213d98918c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('valves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=5), nullable=False),
    sa.Column('size', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Date(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('valve_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['valve_id'], ['valves.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    op.drop_table('valves')
    # ### end Alembic commands ###

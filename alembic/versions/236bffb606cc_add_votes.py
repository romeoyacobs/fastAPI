"""Add votes

Revision ID: 236bffb606cc
Revises: 393dfef2dae1
Create Date: 2022-02-21 12:06:01.575995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '236bffb606cc'
down_revision = '393dfef2dae1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='Cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='Cascade'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###

"""Creating posts table

Revision ID: 4e5e0aa7f5d5
Revises: 
Create Date: 2022-02-20 23:07:23.950152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e5e0aa7f5d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False)
                    )


def downgrade():
    op.drop_table("posts")

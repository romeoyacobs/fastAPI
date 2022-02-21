"""Adding more data to posts

Revision ID: 16a9f803988b
Revises: 4e5e0aa7f5d5
Create Date: 2022-02-20 23:18:11.450872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16a9f803988b'
down_revision = '4e5e0aa7f5d5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade():
    op.drop_column("posts", "content")

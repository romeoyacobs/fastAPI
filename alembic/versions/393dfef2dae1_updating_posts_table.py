"""Updating posts table

Revision ID: 393dfef2dae1
Revises: 16de91cd9cd3
Create Date: 2022-02-21 11:15:37.524177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '393dfef2dae1'
down_revision = '16de91cd9cd3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="Cascade")


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "owner_id")
    op.drop_constraint("post_users_fk", "posts")

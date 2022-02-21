"""Adding users table

Revision ID: 16de91cd9cd3
Revises: 16a9f803988b
Create Date: 2022-02-20 23:29:05.532207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16de91cd9cd3'
down_revision = '16a9f803988b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )


def downgrade():
    op.drop_table("users")

"""Migrates policy to search filters.

Revision ID: 57b1d2ee5a06
Revises: 1adc96915b63
Create Date: 2021-01-21 12:42:28.422473

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "57b1d2ee5a06"
down_revision = "1adc96915b63"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "search_filter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("expression", sa.JSON(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("search_vector", sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["dispatch_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        "ix_search_filter_search_vector",
        "search_filter",
        ["search_vector"],
        unique=False,
        postgresql_using="gin",
    )
    op.add_column("notification", sa.Column("search_filter_id", sa.Integer(), nullable=True))
    op.drop_constraint("notification_policy_id_fkey", "notification", type_="foreignkey")
    op.create_foreign_key(None, "notification", "search_filter", ["search_filter_id"], ["id"])
    op.drop_column("notification", "policy_id")
    op.drop_index("ix_policy_search_vector", table_name="policy")
    op.drop_table("policy")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "notification", sa.Column("policy_id", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "notification", type_="foreignkey")
    op.create_foreign_key(
        "notification_policy_id_fkey", "notification", "policy", ["policy_id"], ["id"]
    )
    op.drop_column("notification", "search_filter_id")
    op.drop_constraint(None, "incident_type", type_="foreignkey")
    op.create_table(
        "policy",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("expression", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("search_vector", postgresql.TSVECTOR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="policy_pkey"),
        sa.UniqueConstraint("name", name="policy_name_key"),
    )
    op.create_index("ix_policy_search_vector", "policy", ["search_vector"], unique=False)
    op.drop_index("ix_search_filter_search_vector", table_name="search_filter")
    op.drop_table("search_filter")
    # ### end Alembic commands ###
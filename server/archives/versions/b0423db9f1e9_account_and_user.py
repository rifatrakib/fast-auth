"""account-and-user.

Revision ID: b0423db9f1e9
Revises:
Create Date: 2023-02-08 09:19:21.479528
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b0423db9f1e9"  # pragma: allowlist secret
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=True),
        sa.Column("hash_salt", sa.String(length=1024), nullable=True),
        sa.Column("phone_number", sa.String(length=16), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_logged_in", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_accounts_email"), "accounts", ["email"], unique=True)
    op.create_index(op.f("ix_accounts_id"), "accounts", ["id"], unique=False)
    op.create_index(op.f("ix_accounts_is_active"), "accounts", ["is_active"], unique=False)
    op.create_index(op.f("ix_accounts_is_logged_in"), "accounts", ["is_logged_in"], unique=False)
    op.create_index(op.f("ix_accounts_is_verified"), "accounts", ["is_verified"], unique=False)
    op.create_index(op.f("ix_accounts_phone_number"), "accounts", ["phone_number"], unique=True)
    op.create_index(op.f("ix_accounts_username"), "accounts", ["username"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("middle_name", sa.String(length=256), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("gender", sa.String(length=1), nullable=True),
        sa.Column("birthday", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_account_id"), "users", ["account_id"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_account_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_accounts_username"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_phone_number"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_is_verified"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_is_logged_in"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_is_active"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_id"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_email"), table_name="accounts")
    op.drop_table("accounts")
    # ### end Alembic commands ###

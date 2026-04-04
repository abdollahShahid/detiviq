"""add day2 core models

Revision ID: 28a146938964
Revises:
Create Date: 2026-04-02
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "28a146938964"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_enum = postgresql.ENUM(
        "admin", "dispatcher", "analyst",
        name="user_role",
        create_type=False,
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_organizations_id", "organizations", ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("role", user_role_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=True),
        sa.Column("customer_name", sa.String(length=255), nullable=True),
        sa.Column("timezone", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "name", name="uq_facility_org_name"),
    )
    op.create_index("ix_facilities_id", "facilities", ["id"], unique=False)
    op.create_index("ix_facility_org_customer", "facilities", ["organization_id", "customer_name"], unique=False)

    op.create_table(
        "loads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("external_reference", sa.String(length=100), nullable=False),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            sa.Enum("planned", "in_transit", "completed", "cancelled", name="load_status"),
            nullable=False,
        ),
        sa.Column("origin_label", sa.String(length=255), nullable=True),
        sa.Column("destination_label", sa.String(length=255), nullable=True),
        sa.Column("scheduled_pickup_at", sa.DateTime(), nullable=True),
        sa.Column("scheduled_delivery_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "external_reference", name="uq_load_org_external_reference"),
    )
    op.create_index("ix_loads_id", "loads", ["id"], unique=False)

    op.create_table(
        "rulesets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "scope_type",
            sa.Enum("facility", "customer", "organization_default", name="ruleset_scope"),
            nullable=False,
        ),
        sa.Column("facility_id", sa.Integer(), nullable=True),
        sa.Column("customer_name", sa.String(length=255), nullable=True),
        sa.Column("free_minutes", sa.Integer(), nullable=False),
        sa.Column("grace_minutes", sa.Integer(), nullable=False),
        sa.Column("billable_unit_minutes", sa.Integer(), nullable=False),
        sa.Column("rate_per_unit", sa.Numeric(10, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("effective_from", sa.DateTime(), nullable=True),
        sa.Column("effective_to", sa.DateTime(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rulesets_id", "rulesets", ["id"], unique=False)

    op.create_table(
        "stops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("load_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("stop_number", sa.Integer(), nullable=False),
        sa.Column("stop_type", sa.Enum("pickup", "delivery", name="stop_type"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("planned", "arrived", "loading", "departed", "completed", name="stop_status"),
            nullable=False,
        ),
        sa.Column("appointment_at", sa.DateTime(), nullable=True),
        sa.Column("actual_arrived_at", sa.DateTime(), nullable=True),
        sa.Column("actual_departed_at", sa.DateTime(), nullable=True),
        sa.Column("current_dwell_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["load_id"], ["loads.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("load_id", "stop_number", name="uq_stop_load_stop_number"),
    )
    op.create_index("ix_stop_load_stop_number", "stops", ["load_id", "stop_number"], unique=False)
    op.create_index("ix_stops_id", "stops", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_stops_id", table_name="stops")
    op.drop_index("ix_stop_load_stop_number", table_name="stops")
    op.drop_table("stops")

    op.drop_index("ix_rulesets_id", table_name="rulesets")
    op.drop_table("rulesets")

    op.drop_index("ix_loads_id", table_name="loads")
    op.drop_table("loads")

    op.drop_index("ix_facility_org_customer", table_name="facilities")
    op.drop_index("ix_facilities_id", table_name="facilities")
    op.drop_table("facilities")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_organizations_id", table_name="organizations")
    op.drop_table("organizations")

    postgresql.ENUM(name="stop_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="stop_type").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="ruleset_scope").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="load_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="user_role").drop(op.get_bind(), checkfirst=True)
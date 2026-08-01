"""Add criteria table

Revision ID: 2c0612a50913
Revises: 2baf251e21a9
Create Date: 2026-08-01 20:57:15.498975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c0612a50913'
down_revision: Union[str, Sequence[str], None] = '2baf251e21a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "criteria",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column(
        "analysis_results",
        sa.Column("criterion_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "analysis_results",
        sa.Column("criterion_name", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "analysis_results",
        sa.Column("criterion_description", sa.Text(), nullable=True),
    )
    op.create_foreign_key(
        "fk_analysis_results_criterion_id_criteria",
        "analysis_results",
        "criteria",
        ["criterion_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("analysis_results", "matched")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "analysis_results",
        sa.Column("matched", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.drop_constraint(
        "fk_analysis_results_criterion_id_criteria",
        "analysis_results",
        type_="foreignkey",
    )
    op.drop_column("analysis_results", "criterion_description")
    op.drop_column("analysis_results", "criterion_name")
    op.drop_column("analysis_results", "criterion_id")

    op.drop_table("criteria")

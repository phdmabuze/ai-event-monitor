"""Add analysis result matches

Revision ID: 553eeada63ad
Revises: 2c0612a50913
Create Date: 2026-08-02 18:32:06.834006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '553eeada63ad'
down_revision: Union[str, Sequence[str], None] = '2c0612a50913'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "analysis_result_matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("analysis_result_id", sa.Integer(), nullable=False),
        sa.Column("criterion_id", sa.Integer(), nullable=False),
        sa.Column("criterion_name", sa.String(length=128), nullable=False),
        sa.Column("criterion_description", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(length=8), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["analysis_result_id"],
            ["analysis_results.id"],
            name="fk_analysis_result_matches_analysis_result_id_analysis_results",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["criterion_id"],
            ["criteria.id"],
            name="fk_analysis_result_matches_criterion_id_criteria",
            ondelete="CASCADE",
        ),
    )

    op.drop_constraint(
        "fk_analysis_results_criterion_id_criteria",
        "analysis_results",
        type_="foreignkey",
    )
    op.drop_column("analysis_results", "criterion_id")
    op.drop_column("analysis_results", "criterion_name")
    op.drop_column("analysis_results", "criterion_description")
    op.drop_column("analysis_results", "reason")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "analysis_results",
        sa.Column("reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "analysis_results",
        sa.Column("criterion_description", sa.Text(), nullable=True),
    )
    op.add_column(
        "analysis_results",
        sa.Column("criterion_name", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "analysis_results",
        sa.Column("criterion_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_analysis_results_criterion_id_criteria",
        "analysis_results",
        "criteria",
        ["criterion_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_table("analysis_result_matches")

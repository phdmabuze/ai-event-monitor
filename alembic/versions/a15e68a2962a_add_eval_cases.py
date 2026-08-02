"""Add eval cases

Revision ID: a15e68a2962a
Revises: 553eeada63ad
Create Date: 2026-08-02 19:31:13.903730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a15e68a2962a'
down_revision: Union[str, Sequence[str], None] = '553eeada63ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "eval_cases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "eval_case_matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("eval_case_id", sa.Integer(), nullable=False),
        sa.Column("criterion_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["eval_case_id"],
            ["eval_cases.id"],
            name="fk_eval_case_matches_eval_case_id_eval_cases",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["criterion_id"],
            ["criteria.id"],
            name="fk_eval_case_matches_criterion_id_criteria",
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("eval_case_matches")
    op.drop_table("eval_cases")

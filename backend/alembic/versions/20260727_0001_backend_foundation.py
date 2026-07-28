from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "20260727_0001"
down_revision = None
branch_labels = None
depends_on = None


def timestamp_columns() -> list[sa.Column]:
    """Return fresh timestamp columns for a table definition."""
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    """Create the Phase 2 backend foundation schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("github_user_id", sa.String(length=64), nullable=True),
        sa.Column("avatar_url", sa.String(length=1024), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("github_user_id"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "organizations",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_organizations_slug", "organizations", ["slug"])

    op.create_table(
        "webhook_deliveries",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("delivery_id", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("repository_full_name", sa.String(length=420), nullable=True),
        sa.Column("commit_sha", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("payload_summary", sa.JSON(), nullable=False),
        sa.UniqueConstraint("delivery_id"),
    )
    op.create_index("ix_webhook_deliveries_delivery_id", "webhook_deliveries", ["delivery_id"])
    op.create_index("ix_webhook_deliveries_event_type", "webhook_deliveries", ["event_type"])
    op.create_index(
        "ix_webhook_deliveries_repository_full_name",
        "webhook_deliveries",
        ["repository_full_name"],
    )
    op.create_index("ix_webhook_deliveries_commit_sha", "webhook_deliveries", ["commit_sha"])

    op.create_table(
        "memberships",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("user_id", "organization_id"),
    )

    op.create_table(
        "repositories",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("github_repo_id", sa.String(length=64), nullable=False),
        sa.Column("owner", sa.String(length=200), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("default_branch", sa.String(length=200), nullable=False),
        sa.Column("clone_url", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("github_repo_id"),
    )
    op.create_index("ix_repositories_github_repo_id", "repositories", ["github_repo_id"])
    op.create_index("ix_repositories_owner", "repositories", ["owner"])
    op.create_index("ix_repositories_name", "repositories", ["name"])

    op.create_table(
        "github_installations",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("github_installation_id", sa.String(length=64), nullable=False),
        sa.Column("account_login", sa.String(length=200), nullable=False),
        sa.Column("account_type", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("github_installation_id"),
    )
    op.create_index(
        "ix_github_installations_account_login",
        "github_installations",
        ["account_login"],
    )

    op.create_table(
        "runs",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("repository_id", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("commit_sha", sa.String(length=64), nullable=False),
        sa.Column("branch", sa.String(length=200), nullable=True),
        sa.Column("webhook_delivery_id", sa.String(length=128), nullable=True),
        sa.Column("plan_summary", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("repository_id", "commit_sha", "event_type"),
        sa.UniqueConstraint("webhook_delivery_id"),
    )
    op.create_index("ix_runs_repository_id", "runs", ["repository_id"])
    op.create_index("ix_runs_event_type", "runs", ["event_type"])
    op.create_index("ix_runs_status", "runs", ["status"])
    op.create_index("ix_runs_commit_sha", "runs", ["commit_sha"])
    op.create_index("ix_runs_webhook_delivery_id", "runs", ["webhook_delivery_id"])

    dependent_tables: Sequence[tuple[str, Sequence[sa.Column]]] = (
        (
            "executions",
            (
                sa.Column("run_id", sa.String(), nullable=False),
                sa.Column("agent_name", sa.String(length=120), nullable=False),
                sa.Column("status", sa.String(length=40), nullable=False),
                sa.Column("webhook_delivery_id", sa.String(length=128), nullable=True),
                sa.Column("input_summary", sa.Text(), nullable=True),
                sa.Column("output_summary", sa.Text(), nullable=True),
                sa.Column("error_message", sa.Text(), nullable=True),
            ),
        ),
        (
            "timeline_events",
            (
                sa.Column("run_id", sa.String(), nullable=False),
                sa.Column("event_type", sa.String(length=80), nullable=False),
                sa.Column("message", sa.Text(), nullable=False),
                sa.Column("metadata_json", sa.JSON(), nullable=False),
            ),
        ),
        (
            "findings",
            (
                sa.Column("run_id", sa.String(), nullable=False),
                sa.Column("category", sa.String(length=80), nullable=False),
                sa.Column("severity", sa.String(length=40), nullable=False),
                sa.Column("title", sa.String(length=300), nullable=False),
                sa.Column("description", sa.Text(), nullable=False),
                sa.Column("file_path", sa.String(length=1024), nullable=True),
                sa.Column("line_number", sa.Integer(), nullable=True),
            ),
        ),
        (
            "pull_requests",
            (
                sa.Column("run_id", sa.String(), nullable=False),
                sa.Column("github_pr_number", sa.Integer(), nullable=True),
                sa.Column("title", sa.String(length=300), nullable=False),
                sa.Column("body", sa.Text(), nullable=False),
                sa.Column("status", sa.String(length=40), nullable=False),
                sa.Column("url", sa.String(length=1024), nullable=True),
            ),
        ),
        (
            "artifacts",
            (
                sa.Column("run_id", sa.String(), nullable=False),
                sa.Column("artifact_type", sa.String(length=80), nullable=False),
                sa.Column("title", sa.String(length=300), nullable=False),
                sa.Column("content", sa.Text(), nullable=False),
                sa.Column("storage_uri", sa.String(length=1024), nullable=True),
            ),
        ),
    )
    for table_name, columns in dependent_tables:
        op.create_table(
            table_name,
            sa.Column("id", sa.String(), primary_key=True),
            *timestamp_columns(),
            *columns,
            sa.ForeignKeyConstraint(["run_id"], ["runs.id"], ondelete="CASCADE"),
        )
    op.create_index("ix_executions_agent_name", "executions", ["agent_name"])
    op.create_index("ix_executions_status", "executions", ["status"])
    op.create_index("ix_executions_webhook_delivery_id", "executions", ["webhook_delivery_id"])
    op.create_index("ix_timeline_events_event_type", "timeline_events", ["event_type"])
    op.create_index("ix_findings_category", "findings", ["category"])
    op.create_index("ix_findings_severity", "findings", ["severity"])
    op.create_index("ix_pull_requests_github_pr_number", "pull_requests", ["github_pr_number"])
    op.create_index("ix_artifacts_artifact_type", "artifacts", ["artifact_type"])

    op.create_table(
        "notifications",
        sa.Column("id", sa.String(), primary_key=True),
        *timestamp_columns(),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("read_at", sa.String(length=40), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["run_id"], ["runs.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    """Drop the Phase 2 backend foundation schema."""
    for table_name in (
        "notifications",
        "artifacts",
        "pull_requests",
        "findings",
        "timeline_events",
        "executions",
        "runs",
        "github_installations",
        "repositories",
        "memberships",
        "webhook_deliveries",
        "organizations",
        "users",
    ):
        op.drop_table(table_name)

"""
Dagster Definitions - dg-managed project with auto-discovery

This module leverages the dg CLI and load_from_defs_folder for complete
auto-discovery of all definitions without any explicit imports.
"""

from pathlib import Path
import dagster as dg
from dagster_snowflake import SnowflakeResource
from dagster.preview.freshness import FreshnessPolicy, apply_freshness_policy
from datetime import timedelta


# Get the project root (where dg.toml is located)
project_root = Path(__file__).parent.parent

# Define resources using Dagster EnvVar for full Dagster+ benefits
snowflake_resource = SnowflakeResource(
    account=dg.EnvVar("SNOWFLAKE_ACCOUNT"),
    user=dg.EnvVar("SNOWFLAKE_USER"), 
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    warehouse=dg.EnvVar("SNOWFLAKE_WAREHOUSE"),
    database=dg.EnvVar("SNOWFLAKE_DATABASE"),
    schema=dg.EnvVar("SNOWFLAKE_SCHEMA"),
    role=dg.EnvVar("SNOWFLAKE_ROLE"),
)

# Default freshness policy for monitoring data staleness
default_freshness_policy = FreshnessPolicy.time_window(
    fail_window=timedelta(hours=48),  # Fail if no update in 2 days
    warn_window=timedelta(hours=24),  # Warn if no update in 1 day
)

# Create the Definitions object with auto-discovery + resources + freshness policies
defs = dg.Definitions.merge(
    dg.load_from_defs_folder(project_root=project_root),  # Load directly without storing
    dg.Definitions(
        resources={
            "snowflake": snowflake_resource,
            # dbt resource managed by dbt component in defs/dbt_analytics/defs.yaml
        }
    )
)

# Apply default freshness policy to all assets (won't override existing policies)
defs = defs.map_asset_specs(
    func=lambda spec: apply_freshness_policy(
        spec, default_freshness_policy, overwrite_existing=False
    ),
)

"""
Job definitions for the Dagster Snowflake dbt demo.

This file defines 4 different job patterns that demonstrate various
orchestration strategies for data pipelines:

1. dbt_models_job - Pure data transformation (dbt only)
2. daily_analytics_job - Full pipeline (dbt + Python analytics)  
3. hourly_metrics_job - Lightweight refreshes (Python analytics only)
4. data_quality_job - Quality validation (asset checks only)
"""

from dagster import define_asset_job, AssetSelection

# Job that runs all dbt models
dbt_models_job = define_asset_job(
    name="dbt_models_job",
    description="Runs all dbt staging and mart models (data transformations only)",
    selection=AssetSelection.groups("tpch_analytics")
)

# Daily analytics job - runs core business metrics
daily_analytics_job = define_asset_job(
    name="daily_analytics_job", 
    description="Daily business analytics pipeline including dbt models and KPI calculations",
    selection=AssetSelection.groups("tpch_analytics", "business_intelligence")
)

# Hourly metrics job - lightweight metrics for dashboards
hourly_metrics_job = define_asset_job(
    name="hourly_metrics_job",
    description="Hourly refresh of key business metrics and trends",
    selection=AssetSelection.assets("business_kpis", "monthly_trends")
)

# Data quality job - runs only asset checks without materializing assets
data_quality_job = define_asset_job(
    name="data_quality_job", 
    description="Comprehensive data quality validation - runs checks only, no asset materialization",
    selection=AssetSelection.checks_for_assets([
        "customer_metrics", 
        "order_analytics", 
        "daily_sales_summary",
        "business_kpis"
    ])
)

# Removed full_refresh_job as it was identical to daily_analytics_job
# In practice, use daily_analytics_job for both scheduled and manual full pipeline runs

"""Schedule definitions for the Dagster Snowflake dbt demo."""

from dagster import ScheduleDefinition
from .jobs import daily_analytics_job, hourly_metrics_job, data_quality_job

# Daily schedule for full analytics pipeline
daily_schedule = ScheduleDefinition(
    job=daily_analytics_job,
    cron_schedule="0 6 * * *",  # 6 AM UTC daily
    name="daily_analytics_schedule",
    description="Runs the daily analytics pipeline every morning at 6 AM UTC"
)

# Hourly schedule for key metrics  
# NOTE: For "business hours only" logic, use cron expressions like "0 9-18 * * 1-5" (weekdays 9 AM - 6 PM)
# rather than sensors - schedules are much better for predictable time-based triggers
hourly_schedule = ScheduleDefinition(
    job=hourly_metrics_job,
    cron_schedule="0 * * * *",  # Every hour (could be "0 9-18 * * 1-5" for business hours only)
    name="hourly_metrics_schedule", 
    description="Updates key business metrics every hour"
)

# Weekly data quality check - checks only, no asset materialization
weekly_data_quality_schedule = ScheduleDefinition(
    job=data_quality_job,
    cron_schedule="0 8 * * 1",  # Monday 8 AM UTC
    name="weekly_data_quality_schedule",
    description="Runs asset checks only - validates data quality without materializing assets"
)

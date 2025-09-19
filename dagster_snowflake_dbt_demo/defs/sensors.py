"""Sensor definitions for the Dagster Snowflake dbt demo."""

from dagster import sensor, DefaultSensorStatus, SensorEvaluationContext, RunRequest, SkipReason
from dagster_snowflake import SnowflakeResource
from .jobs import data_quality_job, hourly_metrics_job
from datetime import datetime, timedelta


# Removed confusing data_freshness_sensor that ran quality checks when data was stale
# 
# Better alternatives for data freshness monitoring:
# 1. Asset freshness policies (enable in dagster.yaml: {"asset_metadata": {"enabled": true}})
# 2. Scheduled data quality checks (see schedules.py - weekly_data_quality_schedule)  
# 3. Asset sensors that trigger refreshes when upstream data changes


# Example sensor demonstrating event-driven orchestration patterns
# 
# NOTE: This is a simplified demo sensor. In production, you'd typically use:
# - File sensors (monitoring S3 buckets, file systems)  
# - Asset sensors (triggering when upstream assets change)
# - External system sensors (monitoring APIs, databases)
# - Slack/webhook sensors (responding to external events)

@sensor(
    job=hourly_metrics_job,
    name="demo_conditional_sensor",
    description="Demo sensor showing conditional logic - normally you'd monitor external systems",
    default_status=DefaultSensorStatus.STOPPED  # Disabled by default - this is just for demo
)
def demo_conditional_sensor(context: SensorEvaluationContext):
    """
    DEMO ONLY: Shows sensor patterns like conditional logic and run keys.
    
    Real sensors would monitor:
    - New files in S3/blob storage 
    - Changes in external databases
    - Webhook notifications from external systems
    - Asset materialization events
    """
    current_hour = datetime.now().hour
    
    # Demo condition: Only during "business hours" 
    # (In reality, this should just be a schedule!)
    if 9 <= current_hour <= 18:
        run_key = f"demo_conditional_{datetime.now().strftime('%Y-%m-%d-%H')}"
        
        return RunRequest(
            run_key=run_key,
            tags={
                "trigger": "demo_conditional",
                "hour": str(current_hour),
                "note": "This should be a schedule, not a sensor!"
            }
        )
    else:
        return SkipReason(f"Demo condition not met (hour: {current_hour})")


# No manual exports needed - dg auto-discovery handles sensor discovery

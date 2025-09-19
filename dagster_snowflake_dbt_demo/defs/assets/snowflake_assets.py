"""Snowflake-specific assets for the demo."""

from typing import Dict, Any
import pandas as pd
from dagster import asset, AssetExecutionContext, MetadataValue, AssetCheckSpec, AssetCheckResult
from dagster_snowflake import SnowflakeResource
from dagster.preview.freshness import FreshnessPolicy
from datetime import timedelta


@asset(
    description="Business KPIs calculated from dbt mart models using Snowflake queries with Python processing",
    kinds={"python", "snowflake"},  # Both Python processing and Snowflake queries
    group_name="business_intelligence",
    deps=["customer_metrics", "order_analytics", "daily_sales_summary"],
    # Time window freshness policy - this critical asset should be updated every 2 hours
    freshness_policy=FreshnessPolicy.time_window(
        fail_window=timedelta(hours=4),   # Fail if not updated in 4 hours
        warn_window=timedelta(hours=2),   # Warn if not updated in 2 hours  
    )
)
def business_kpis(context: AssetExecutionContext, snowflake: SnowflakeResource) -> Dict[str, Any]:
    """
    Calculate key business metrics from the dbt mart models.
    Demonstrates asset dependencies and business logic.
    """
    
    kpi_queries = {
        "total_revenue": "SELECT SUM(total_revenue) FROM daily_sales_summary",
        "total_customers": "SELECT COUNT(DISTINCT customer_key) FROM customer_metrics",
        "avg_order_value": "SELECT AVG(total_revenue / NULLIF(orders_count, 0)) FROM daily_sales_summary",
        "high_value_customers": "SELECT COUNT(*) FROM customer_metrics WHERE customer_value_segment = 'High Value'",
        "active_customers": "SELECT COUNT(*) FROM customer_metrics WHERE customer_status = 'Active'",
        "churn_rate": """
            SELECT 
                (COUNT(CASE WHEN customer_status = 'Churned' THEN 1 END) * 100.0 / 
                 NULLIF(COUNT(CASE WHEN customer_status IN ('Active', 'At Risk', 'Churned') THEN 1 END), 0))
            FROM customer_metrics
        """
    }
    
    kpis = {}
    with snowflake.get_connection() as conn:
        for kpi_name, query in kpi_queries.items():
            try:
                result = conn.execute_query(query)
                if result and result[0][0] is not None:
                    kpis[kpi_name] = float(result[0][0])
                else:
                    kpis[kpi_name] = 0.0
            except Exception as e:
                context.log.warning(f"Failed to calculate {kpi_name}: {str(e)}")
                kpis[kpi_name] = 0.0
    
    # Add metadata
    context.add_output_metadata({
        "total_revenue": MetadataValue.float(kpis.get("total_revenue", 0)),
        "total_customers": MetadataValue.int(int(kpis.get("total_customers", 0))),
        "avg_order_value": MetadataValue.float(round(kpis.get("avg_order_value", 0), 2)),
        "high_value_customers": MetadataValue.int(int(kpis.get("high_value_customers", 0))),
        "active_customers": MetadataValue.int(int(kpis.get("active_customers", 0))),
        "churn_rate_percent": MetadataValue.float(round(kpis.get("churn_rate", 0), 2)),
    })
    
    return kpis


@asset(
    description="Monthly trend analysis for executive reporting using Snowflake aggregation with Python DataFrame processing",
    kinds={"python", "snowflake"},  # Both Python DataFrame processing and Snowflake queries
    group_name="business_intelligence",
    deps=["daily_sales_summary"]
)
def monthly_trends(context: AssetExecutionContext, snowflake: SnowflakeResource) -> pd.DataFrame:
    """
    Generate monthly trend analysis from daily sales data.
    Returns a pandas DataFrame for further analysis.
    """
    query = """
    SELECT 
        order_year,
        order_month,
        SUM(total_revenue) as monthly_revenue,
        SUM(orders_count) as monthly_orders,
        SUM(unique_customers) as monthly_customers,
        AVG(avg_order_value) as avg_monthly_order_value
    FROM daily_sales_summary
    GROUP BY order_year, order_month
    ORDER BY order_year, order_month
    """
    
    with snowflake.get_connection() as conn:
        result = conn.execute_query(query)
    
    if result:
        df = pd.DataFrame(result, columns=[
            'year', 'month', 'revenue', 'orders', 'customers', 'avg_order_value'
        ])
        
        # Calculate month-over-month growth
        df['revenue_growth'] = df['revenue'].pct_change() * 100
        df['orders_growth'] = df['orders'].pct_change() * 100
        
        context.add_output_metadata({
            "num_months": MetadataValue.int(len(df)),
            "avg_monthly_revenue": MetadataValue.float(round(df['revenue'].mean(), 2)),
            "max_monthly_revenue": MetadataValue.float(round(df['revenue'].max(), 2)),
            "avg_revenue_growth": MetadataValue.float(round(df['revenue_growth'].mean(), 2)),
            "preview": MetadataValue.md(df.head().to_markdown())
        })
        
        return df
    else:
        return pd.DataFrame()


# Asset checks for data quality
# Removed confusing data_quality_checks asset - use asset_checks.py for proper DQ validation


# No manual exports needed - dg auto-discovery handles asset discovery

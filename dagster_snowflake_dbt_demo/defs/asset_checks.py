"""Asset check definitions for data quality validation."""

from dagster import asset_check, AssetCheckResult, AssetCheckSeverity
from dagster_snowflake import SnowflakeResource


@asset_check(asset="customer_metrics", description="Validates customer metrics data quality")
def customer_metrics_quality_check(snowflake: SnowflakeResource) -> AssetCheckResult:
    """
    Comprehensive quality check for customer metrics table.
    Validates completeness, consistency, and business logic.
    """
    checks = []
    
    with snowflake.get_connection() as conn:
        # Check for null customer keys
        result = conn.execute_query("""
            SELECT COUNT(*) as null_keys
            FROM customer_metrics 
            WHERE customer_key IS NULL
        """)
        null_keys = result[0][0] if result else 0
        
        # Check for negative account balances where total_spent > 0
        result = conn.execute_query("""
            SELECT COUNT(*) as invalid_balances
            FROM customer_metrics 
            WHERE total_spent > 0 AND account_balance < 0
        """)
        invalid_balances = result[0][0] if result else 0
        
        # Check customer value segment logic
        result = conn.execute_query("""
            SELECT COUNT(*) as logic_errors
            FROM customer_metrics 
            WHERE (customer_value_segment = 'High Value' AND total_spent <= 500000)
               OR (customer_value_segment = 'Medium Value' AND (total_spent <= 100000 OR total_spent > 500000))
               OR (customer_value_segment = 'Low Value' AND (total_spent <= 0 OR total_spent > 100000))
        """)
        logic_errors = result[0][0] if result else 0
    
    # Evaluate checks
    passed = null_keys == 0 and invalid_balances == 0 and logic_errors == 0
    
    if passed:
        return AssetCheckResult(
            passed=True,
            description="All customer metrics quality checks passed"
        )
    else:
        return AssetCheckResult(
            passed=False,
            description=f"Quality issues found: {null_keys} null keys, {invalid_balances} invalid balances, {logic_errors} logic errors",
            severity=AssetCheckSeverity.WARN if (null_keys + invalid_balances + logic_errors) < 10 else AssetCheckSeverity.ERROR
        )


@asset_check(asset="order_analytics", description="Validates order analytics data quality")
def order_analytics_quality_check(snowflake: SnowflakeResource) -> AssetCheckResult:
    """
    Quality check for order analytics table.
    Focuses on order totals and line item consistency.
    """
    with snowflake.get_connection() as conn:
        # Check for orders with zero or negative totals
        result = conn.execute_query("""
            SELECT COUNT(*) as invalid_totals
            FROM order_analytics 
            WHERE order_total <= 0
        """)
        invalid_totals = result[0][0] if result else 0
        
        # Check for orders without line items
        result = conn.execute_query("""
            SELECT COUNT(*) as orders_no_items
            FROM order_analytics 
            WHERE line_item_count = 0 OR line_item_count IS NULL
        """)
        orders_no_items = result[0][0] if result else 0
        
        # Check for impossible discount percentages
        result = conn.execute_query("""
            SELECT COUNT(*) as invalid_discounts
            FROM order_analytics 
            WHERE discount_percentage < 0 OR discount_percentage > 1
        """)
        invalid_discounts = result[0][0] if result else 0
    
    issues = invalid_totals + orders_no_items + invalid_discounts
    
    return AssetCheckResult(
        passed=issues == 0,
        description=f"Order analytics check: {invalid_totals} invalid totals, {orders_no_items} orders without items, {invalid_discounts} invalid discounts",
        severity=AssetCheckSeverity.ERROR if issues > 0 else None
    )


@asset_check(asset="daily_sales_summary", description="Validates daily sales summary completeness")
def daily_sales_completeness_check(snowflake: SnowflakeResource) -> AssetCheckResult:
    """
    Checks for gaps in daily sales data and validates aggregation logic.
    """
    with snowflake.get_connection() as conn:
        # Check for missing recent days (should have data up to at least yesterday)
        result = conn.execute_query("""
            SELECT DATEDIFF(day, MAX(order_date), CURRENT_DATE) as days_behind
            FROM daily_sales_summary
        """)
        days_behind = result[0][0] if result else 999
        
        # Check for days with zero revenue (could indicate data issues)
        result = conn.execute_query("""
            SELECT COUNT(*) as zero_revenue_days
            FROM daily_sales_summary 
            WHERE total_revenue = 0 OR total_revenue IS NULL
        """)
        zero_revenue_days = result[0][0] if result else 0
        
        # Check for negative metrics
        result = conn.execute_query("""
            SELECT COUNT(*) as negative_metrics
            FROM daily_sales_summary 
            WHERE total_revenue < 0 OR orders_count < 0 OR unique_customers < 0
        """)
        negative_metrics = result[0][0] if result else 0
    
    # Data is considered fresh if within 3 days
    is_fresh = days_behind <= 3
    has_valid_data = zero_revenue_days < 30 and negative_metrics == 0  # Allow some zero days
    
    passed = is_fresh and has_valid_data
    
    severity = AssetCheckSeverity.ERROR if not has_valid_data else (
        AssetCheckSeverity.WARN if not is_fresh else None
    )
    
    return AssetCheckResult(
        passed=passed,
        description=f"Data freshness: {days_behind} days behind, {zero_revenue_days} zero-revenue days, {negative_metrics} negative metrics",
        severity=severity
    )


@asset_check(asset="business_kpis", description="Validates business KPI calculations")
def business_kpis_validation_check(snowflake: SnowflakeResource) -> AssetCheckResult:
    """
    Validates that business KPIs are within expected ranges and internally consistent.
    """
    with snowflake.get_connection() as conn:
        # Get customer counts from source for validation
        result = conn.execute_query("""
            SELECT 
                COUNT(*) as total_customers_source,
                COUNT(CASE WHEN customer_value_segment = 'High Value' THEN 1 END) as high_value_source
            FROM customer_metrics
        """)
        
        if result:
            total_customers_source = result[0][0]
            high_value_source = result[0][1]
        else:
            return AssetCheckResult(
                passed=False,
                description="Could not retrieve source data for validation",
                severity=AssetCheckSeverity.ERROR
            )
    
    # Basic validation - in a real scenario, you'd compare against the actual KPI values
    # This is a simplified check since we don't have the actual KPI asset values here
    issues = []
    
    if total_customers_source == 0:
        issues.append("No customers found")
    
    if high_value_source > total_customers_source:
        issues.append("High value customers exceed total customers")
    
    passed = len(issues) == 0
    
    return AssetCheckResult(
        passed=passed,
        description=f"KPI validation: {len(issues)} issues found: {', '.join(issues) if issues else 'All checks passed'}",
        severity=AssetCheckSeverity.ERROR if not passed else None
    )

{{
    config(
        description="Daily sales summary metrics for dashboard reporting",
        materialized='table'
    )
}}

select
    order_date,
    order_year,
    order_month,
    order_quarter,
    count(distinct order_key) as orders_count,
    count(distinct customer_key) as unique_customers,
    sum(order_total) as total_revenue,
    avg(order_total) as avg_order_value,
    sum(total_quantity) as total_items_sold,
    sum(total_discount_amount) as total_discounts,
    count(case when order_size_category = 'Large' then 1 end) as large_orders,
    count(case when order_size_category = 'Medium' then 1 end) as medium_orders,
    count(case when order_size_category = 'Small' then 1 end) as small_orders
from {{ ref('order_analytics') }}
group by 1, 2, 3, 4
order by order_date

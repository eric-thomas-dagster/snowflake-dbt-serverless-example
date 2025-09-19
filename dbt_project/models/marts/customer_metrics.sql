{{
    config(
        description="Customer-level metrics and analytics",
        materialized='table'
    )
}}

with customer_orders as (
    select
        c.customer_key,
        c.customer_name,
        c.market_segment,
        c.account_balance,
        count(o.order_key) as total_orders,
        sum(o.total_price) as total_spent,
        avg(o.total_price) as avg_order_value,
        min(o.order_date) as first_order_date,
        max(o.order_date) as last_order_date,
        count(distinct date_trunc('month', o.order_date)) as active_months
    from {{ ref('stg_customers') }} c
    left join {{ ref('stg_orders') }} o 
        on c.customer_key = o.customer_key
    group by 1, 2, 3, 4
),

customer_segments as (
    select
        *,
        case 
            when total_spent > 500000 then 'High Value'
            when total_spent > 100000 then 'Medium Value'
            when total_spent > 0 then 'Low Value'
            else 'No Orders'
        end as customer_value_segment,
        case
            when last_order_date >= current_date - interval '90 days' then 'Active'
            when last_order_date >= current_date - interval '365 days' then 'At Risk'
            when last_order_date is not null then 'Churned'
            else 'Never Ordered'
        end as customer_status
    from customer_orders
)

select * from customer_segments

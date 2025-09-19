{{
    config(
        description="Order-level analytics with line item details",
        materialized='table'
    )
}}

with order_details as (
    select
        o.order_key,
        o.customer_key,
        o.order_status,
        o.order_date,
        o.order_priority,
        o.total_price as order_total,
        count(l.line_number) as line_item_count,
        sum(l.quantity) as total_quantity,
        sum(l.extended_price * (1 - l.discount) * (1 + l.tax)) as calculated_total,
        avg(l.discount) as avg_discount,
        sum(l.extended_price * l.discount) as total_discount_amount
    from {{ ref('stg_orders') }} o
    left join {{ ref('stg_lineitems') }} l 
        on o.order_key = l.order_key
    group by 1, 2, 3, 4, 5, 6
),

order_metrics as (
    select
        *,
        extract(year from order_date) as order_year,
        extract(month from order_date) as order_month,
        extract(quarter from order_date) as order_quarter,
        date_trunc('month', order_date) as order_month_year,
        case 
            when order_total > 100000 then 'Large'
            when order_total > 10000 then 'Medium'
            else 'Small'
        end as order_size_category,
        total_discount_amount / nullif(order_total, 0) as discount_percentage
    from order_details
)

select * from order_metrics

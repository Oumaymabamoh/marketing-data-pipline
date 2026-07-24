with source as (
    select * from {{ source('raw', 'transactions') }}
)

select
    transaction_id,
    customer_id,
    timestamp::timestamp as transaction_at,
    channel_source as channel,
    product_id,
    product_name,
    product_category,
    quantity::int as quantity,
    gross_revenue::double as gross_revenue,
    is_returned::boolean as is_returned,
    -- Calculate net revenue logic directly at staging level
    case
        when is_returned then 0
        else gross_revenue
    end as net_revenue
from source
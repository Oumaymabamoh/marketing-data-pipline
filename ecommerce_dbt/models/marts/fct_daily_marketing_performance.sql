with ads as (
    select
        ad_date,
        channel,
        sum(impressions) as total_impressions,
        sum(clicks) as total_clicks,
        sum(ad_spend) as total_spend
    from {{ ref('stg_ad_performance') }}
    group by 1, 2
),

tx as (
    select
        transaction_at::date as order_date,
        channel,
        count(distinct transaction_id) as total_orders,
        sum(quantity) as items_sold,
        sum(gross_revenue) as gross_revenue,
        sum(net_revenue) as net_revenue
    from {{ ref('stg_transactions') }}
    group by 1, 2
)

select
    coalesce(a.ad_date, t.order_date) as metric_date,
    coalesce(a.channel, t.channel) as channel,
    coalesce(a.total_impressions, 0) as total_impressions,
    coalesce(a.total_clicks, 0) as total_clicks,
    coalesce(a.total_spend, 0) as total_spend,
    coalesce(t.total_orders, 0) as total_orders,
    coalesce(t.items_sold, 0) as items_sold,
    coalesce(t.gross_revenue, 0) as total_gross_revenue,
    coalesce(t.net_revenue, 0) as total_net_revenue,
    -- Calculate Return on Ad Spend (ROAS)
    round(
        coalesce(t.net_revenue, 0) / nullif(coalesce(a.total_spend, 0), 0),
        2
    ) as roas
from ads a
full outer join tx t
    on a.ad_date = t.order_date
   and a.channel = t.channel
with source as (
    select * from {{ source('raw', 'ad_performance') }}
)

select
    date::date as ad_date,
    campaign_id,
    channel,
    ad_creative,
    impressions::int as impressions,
    clicks::int as clicks,
    spend::double as ad_spend
from source
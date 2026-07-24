import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()


def generate_daily_marketing_data(execution_date=None):
    if not execution_date:
        execution_date = datetime.now().strftime("%Y-%m-%d")

    channels = ["Google_Search", "Meta_Instagram", "TikTok_Ads", "YouTube_Video"]

    # 1. Generate Ad Campaign Performance Data
    ad_data = []
    for channel in channels:
        impressions = random.randint(10000, 50000)
        # CTR varies by platform
        ctr = random.uniform(0.015, 0.045)
        clicks = int(impressions * ctr)
        cpc = random.uniform(0.50, 3.50)
        spend = round(clicks * cpc, 2)

        ad_data.append(
            {
                "date": execution_date,
                "campaign_id": f"CMP_{channel[:3].upper()}_{random.randint(100, 999)}",
                "channel": channel,
                "impressions": impressions,
                "clicks": clicks,
                "spend": spend,
            }
        )

    df_ads = pd.DataFrame(ad_data)

    # 2. Generate User Conversions / Transactions Data
    conversions_data = []
    total_clicks = df_ads["clicks"].sum()
    num_conversions = int(
        total_clicks * random.uniform(0.02, 0.05)
    )  # 2-5% conversion rate

    for _ in range(num_conversions):
        conversions_data.append(
            {
                "transaction_id": fake.uuid4(),
                "customer_id": f"CUST_{random.randint(1000, 9999)}",
                "timestamp": f"{execution_date} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                "channel": random.choice(channels),
                "order_value": round(np.random.exponential(scale=60) + 10, 2),
            }
        )

    df_conversions = pd.DataFrame(conversions_data)

    return df_ads, df_conversions


# Test execution
df_ads, df_conversions = generate_daily_marketing_data()
print("--- Daily Ad Performance ---")
print(df_ads.head())
print("\n--- Daily User Transactions ---")
print(df_conversions.head())
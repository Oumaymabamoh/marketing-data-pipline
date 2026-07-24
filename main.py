import random
from datetime import datetime
import numpy as np
import pandas as pd
from faker import Faker
import duckdb
fake = Faker()

# Define company-specific product catalog
PRODUCT_CATALOG = [
    {
        "product_id": "PROD_001",
        "name": "Ultraboost Running Shoes",
        "category": "Footwear",
        "price": 180.00,
    },
    {
        "product_id": "PROD_002",
        "name": "Samba OG Sneakers",
        "category": "Footwear",
        "price": 100.00,
    },
    {
        "product_id": "PROD_003",
        "name": "Tiro Track Pants",
        "category": "Apparel",
        "price": 55.00,
    },
    {
        "product_id": "PROD_004",
        "name": "Essential Trefoil Hoodie",
        "category": "Apparel",
        "price": 65.00,
    },
    {
        "product_id": "PROD_005",
        "name": "Performance Ankle Socks (3 Pack)",
        "category": "Accessories",
        "price": 18.00,
    },
]

CAMPAIGN_CREATIVES = [
    "Summer Clearance 30% Off",
    "Run Like the Wind - New Ultraboost",
    "Back to School Essentials",
    "Streetwear Classics - Samba Collection",
]


def generate_daily_ecommerce_data(execution_date=None):
    if not execution_date:
        execution_date = datetime.now().strftime("%Y-%m-%d")

    channels = ["Google_Search", "Meta_Instagram", "TikTok_Ads", "YouTube_Video"]

    # --- 1. Ad Campaign Performance Data ---
    ad_data = []
    for channel in channels:
        creative = random.choice(CAMPAIGN_CREATIVES)
        impressions = random.randint(15000, 60000)
        ctr = random.uniform(0.012, 0.048)
        clicks = int(impressions * ctr)
        cpc = random.uniform(0.60, 2.80)
        spend = round(clicks * cpc, 2)

        ad_data.append(
            {
                "date": execution_date,
                "campaign_id": f"CMP_{channel[:3].upper()}_{random.randint(100, 999)}",
                "channel": channel,
                "ad_creative": creative,
                "impressions": impressions,
                "clicks": clicks,
                "spend": spend,
            }
        )

    df_ads = pd.DataFrame(ad_data)

    # --- 2. Customer Transactions & E-commerce Data ---
    conversions_data = []
    total_clicks = df_ads["clicks"].sum()
    num_conversions = int(
        total_clicks * random.uniform(0.02, 0.045)
    )  # 2% - 4.5% conversion rate

    for _ in range(num_conversions):
        product = random.choice(PRODUCT_CATALOG)
        quantity = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
        gross_revenue = product["price"] * quantity

        # Simulate returns (Apparel/Shoes have a ~15% return rate in real world)
        is_returned = random.choices([True, False], weights=[0.15, 0.85])[0]

        conversions_data.append(
            {
                "transaction_id": f"TRX_{fake.uuid4()[:8].upper()}",
                "customer_id": f"CUST_{random.randint(1000, 3000)}",  # Overlapping customer IDs create repeat buyers!
                "timestamp": f"{execution_date} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                "channel_source": random.choice(channels),
                "product_id": product["product_id"],
                "product_name": product["name"],
                "product_category": product["category"],
                "quantity": quantity,
                "gross_revenue": gross_revenue,
                "is_returned": is_returned,
            }
        )

    df_transactions = pd.DataFrame(conversions_data)

    return df_ads, df_transactions


# Test the generator
df_ads, df_transactions = generate_daily_ecommerce_data()


# --- DUCKDB DATA WAREHOUSE INGESTION ---

# 1. Connect to (or create) local database file
conn = duckdb.connect("analytics.duckdb")

# 2. Create schema for raw/staging data
conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")

# 3. Write DataFrames directly into DuckDB SQL tables
conn.execute(
    "CREATE TABLE IF NOT EXISTS raw.ad_performance AS SELECT * FROM df_ads WHERE 1=0;"
)
conn.execute("INSERT INTO raw.ad_performance SELECT * FROM df_ads;")

conn.execute(
    "CREATE TABLE IF NOT EXISTS raw.transactions AS SELECT * FROM df_transactions WHERE 1=0;"
)
conn.execute("INSERT INTO raw.transactions SELECT * FROM df_transactions;")

print("✅ Data successfully pushed into local DuckDB Data Warehouse!")

# Quick check to prove tables exist
tables = conn.execute("SHOW TABLES FROM raw;").fetchall()
print("Tables created in raw schema:", tables)

conn.close()
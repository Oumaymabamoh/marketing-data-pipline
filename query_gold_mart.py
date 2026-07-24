import duckdb

conn = duckdb.connect("analytics.duckdb")

# Query the gold-layer data mart built by dbt
df = conn.execute("""
    SELECT 
        metric_date,
        channel,
        total_spend,
        total_orders,
        total_gross_revenue,
        total_net_revenue,
        roas
    FROM fct_daily_marketing_performance
    ORDER BY total_net_revenue DESC;
""").df()

print("--- 🏆 EXECUTIVE GOLD MART: MARKETING & ROAS PERFORMANCE 🏆 ---")
print(df)

conn.close()
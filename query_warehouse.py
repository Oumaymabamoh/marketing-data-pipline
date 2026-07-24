import duckdb

conn = duckdb.connect("analytics.duckdb")

# Run an SQL query on your data warehouse
sql_query = """
SELECT 
    channel_source,
    COUNT(transaction_id) as total_orders,
    ROUND(SUM(gross_revenue), 2) as total_gross_revenue,
    SUM(CASE WHEN is_returned THEN 1 ELSE 0 END) as total_returns
FROM raw.transactions
GROUP BY channel_source
ORDER BY total_gross_revenue DESC;
"""

print(conn.execute(sql_query).df())
conn.close()
import duckdb

conn = duckdb.connect("analytics.duckdb")

# List all schemas and tables in DuckDB
print("--- ALL SCHEMAS AND TABLES IN DUCKDB ---")
print(
    conn.execute(
        "SELECT table_schema, table_name FROM information_schema.tables;"
    ).df()
)

conn.close()
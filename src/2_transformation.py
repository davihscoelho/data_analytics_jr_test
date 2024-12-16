import duckdb


duckdb_conn = duckdb.connect("data.db")
duckdb_conn.execute("INSTALL sqlite_scanner;")
duckdb_conn.execute("LOAD sqlite_scanner;")
duckdb_conn.execute(f"SELECT sqlite_attach('test_analytics.db');")

duckdb_conn.execute(
  """
  CREATE SCHEMA IF NOT EXISTS teste.raw;
  CREATE SCHEMA IF NOT EXISTS teste.stg;
  CREATE SCHEMA IF NOT EXISTS teste.mart;
  """
)

tables = duckdb_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

for table in tables:
    table_name = table[0]
    duckdb_conn.execute(f"CREATE TABLE raw.{table_name} AS SELECT * FROM sqlite_scan('{table_name}')")

duckdb_conn.close()
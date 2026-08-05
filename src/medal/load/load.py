import duckdb
from pathlib import Path

Connection = duckdb.DuckDBPyConnection

def connect(db_path: str = "datalake.db") -> Connection:
    """Estabelece uma conexão com o banco de dados DuckDB."""
    return duckdb.connect(db_path)

def ensure_schema(conn: Connection, schema: str) -> None:
    """Garante que o schema especificado exista no banco de dados."""
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

def create_table(
        conn: Connection, 
        sql_path: str, 
        table_name: str, 
        zone: str = "gold"
) -> None:
    """Cria tabelas no Banco de Dados a partir de queries SQL."""
    ensure_schema(conn, zone)

    query = Path(sql_path).read_text(encoding="utf-8").strip.rstrip(";")
    conn.execute(f"""
    CREATE OR REPLACE TABLE {zone}.{table_name} AS
    {query}
    """)
    
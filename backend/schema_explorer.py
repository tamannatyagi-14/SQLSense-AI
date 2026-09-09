import sqlite3

def get_schema_info():
    conn = sqlite3.connect("database/sample.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]

    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns_raw = cursor.fetchall()
        columns = [{"name": col[1], "type": col[2]} for col in columns_raw]

        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        sample_rows = cursor.fetchall()

        schema[table] = {
            "columns": columns,
            "sample_rows": sample_rows
        }

    conn.close()
    return schema
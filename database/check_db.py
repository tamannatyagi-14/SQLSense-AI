import sqlite3

conn = sqlite3.connect("database/sample.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", tables)

cursor.execute("SELECT * FROM employee_details LIMIT 5")
rows = cursor.fetchall()
print("\nSample data from view:")
for row in rows:
    print(row)

conn.close()
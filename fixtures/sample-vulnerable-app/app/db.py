import sqlite3

def find_user(conn: sqlite3.Connection, username: str):
    # VULN: SQL built by string formatting
    query = "SELECT * FROM users WHERE name = '%s'" % username
    return conn.execute(query).fetchall()

def find_order(conn, order_id):
    return conn.cursor().execute(f"SELECT * FROM orders WHERE id = {order_id}")

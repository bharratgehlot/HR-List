# verify_data.py
from postgres_sql import get_connection
import psycopg2.extras

def verify():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT COUNT(*) as count FROM contacts;")
    result = cursor.fetchone()
    print(f"Total contacts: {result['count']}")
    conn.close()

if __name__ == '__main__':
    verify()

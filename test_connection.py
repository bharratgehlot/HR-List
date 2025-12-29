import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_connection():
  try:
    database_url = os.getenv('DATABASE_URL')
    print("Testing database connection to {database_url} ")

    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    # Test Basic Queries

    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Connected successfully!")
    print(f"PostgreSQL version: {version[0]}")

    # Test if contacts table exists

    cursor.execute("""
         SELECT EXISTS (
           SELECT FROM information_schema.tables
           WHERE table_name = 'contacts'
         );
     """)
    table_exists = cursor.fetchone()[0]
    print(f"Contact table exists: {table_exists} ")
    conn.close()
    return True
  
  except Exception as e:
    print(f"Connection failed: {e}")
    return False
  
if __name__ == '__main__':
  test_connection()  
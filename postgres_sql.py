from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection_local():
  return psycopg2.connect(
            host='localhost',
            port='5432',
            database='hr_list',
            user='postgres',
            password=12345678
  )

def get_connection():
    database_url = os.getenv('DATABASE_URL')
    if  not database_url:
        raise ValueError("Database URL not found")
    return psycopg2.connect(database_url)
  

def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                photo VARCHAR(500),
                name VARCHAR(255) NOT NULL,
                company VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                position VARCHAR(255),
                number VARCHAR(20) NOT NULL,
                email VARCHAR(255) NOT NULL,
                status VARCHAR(50) NOT NULL,
                url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        print("✅ Table 'contacts' created successfully!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")

def insert_contact(photo, name, company, location, position, number, email, status, url):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacts (photo, name, company, location, position, number, email, status, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (photo, name, company, location, position, number, email, status, url))
        conn.commit()
        conn.close()
        print(f"✅ Contact '{name}' added!")
    except Exception as e:
        print(f"❌ Failed to add contact: {e}")
        

if __name__ == '__main__':
    create_table()

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
        
def insert_sample_data():
    sample_contacts = [
        ('/uploads/1759939000288_Titiksha_Patil_.jpg', 'Titiksha Patil', 'ITGeeks', 'Dewas', 'HR Manager', '9244123562', 'hrd@itgeeks.com', 'active', 'https://itgeeks.com'),
        ('/uploads/1760152890_Bharrat_Gehlot.jpg', 'Bharrat Gehlot', 'Net-Flow Solutions', 'Sreyal Namkin', 'Developer', '9244123562', 'bharratgehlot@proton.me', 'not active', 'https://netflow.com'),
        (None, 'John Smith', 'Tech Corp', 'Mumbai', 'Recruiter', '9876543210', 'john@techcorp.com', 'active', 'https://techcorp.com'),
        (None, 'Sarah Johnson', 'StartupXYZ', 'Bangalore', 'Talent Acquisition', '8765432109', 'sarah@startupxyz.com', 'active', 'https://startupxyz.com'),
        (None, 'Mike Wilson', 'Global Tech', 'Delhi', 'HR Director', '7654321098', 'mike@globaltech.com', 'status unknown', 'https://globaltech.com')
    ]
    
    for contact in sample_contacts:
        insert_contact(*contact)
        
        

if __name__ == '__main__':
    create_table()
    insert_sample_data()
import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("Database URL not found")
    return psycopg2.connect(database_url)

def import_from_json():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        for contact in data['contacts']:
            cursor.execute("""
                INSERT INTO contacts (photo, name, company, location, position, number, email, status, url, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                contact['photo'],
                contact['name'],
                contact['company'],
                contact['location'],
                contact['position'],
                contact['number'],
                contact['email'],
                contact['status'],
                contact['url'],
                contact['created_at']
            ))
            print(f"✅ Imported: {contact['name']}")
        
        conn.commit()
        conn.close()
        print(f"✅ Successfully imported {len(data['contacts'])} contacts!")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")

if __name__ == '__main__':
    import_from_json()
import os
from postgres_sql import get_connection
import psycopg2.extras

def test_photo_files():
    # Get photo paths from database
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT name, photo FROM contacts WHERE photo IS NOT NULL;")
    contacts = cursor.fetchall()
    conn.close()
    
    print("Checking photo files:")
    print("-" * 50)
    
    for contact in contacts:
        photo_path = contact['photo']
        if photo_path:
            # Remove leading slash and check if file exists
            file_path = photo_path.lstrip('/')
            full_path = os.path.join(file_path)
            
            exists = os.path.exists(full_path)
            status = "EXISTS" if exists else "MISSING"
            
            print(f"{contact['name']:<20} | {status}")
            print(f"{'':>20} | DB Path: {photo_path}")
            print(f"{'':>20} | File Path: {full_path}")
            print()

if __name__ == '__main__':
    test_photo_files()
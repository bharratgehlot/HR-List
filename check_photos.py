from postgres_sql import get_connection
import psycopg2.extras

def check_photo_data():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT name, photo FROM contacts ORDER BY created_at DESC;")
        contacts = cursor.fetchall()
        conn.close()
        
        print("Photo data in database:")
        print("-" * 50)
        for contact in contacts:
            photo_status = "HAS PHOTO" if contact['photo'] else "NO PHOTO"
            print(f"{contact['name']:<20} | {photo_status}")
            if contact['photo']:
                print(f"{'':>20} | Path: {contact['photo']}")
        
        print(f"\nTotal contacts: {len(contacts)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_photo_data()
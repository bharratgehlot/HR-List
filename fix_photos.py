from postgres_sql import get_connection

def fix_photo_paths():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Update existing contacts to use available photos
    updates = [
        ("Titiksha Patil", "/uploads/one.jpg"),
        ("Bharrat Gehlot", "/uploads/two.jpg"), 
        ("Niharika Sharma", "/uploads/three.jpg"),
        ("Rangoli Bhatt", "/uploads/four.jpg")
    ]
    
    for name, photo_path in updates:
        cursor.execute(
            "UPDATE contacts SET photo = %s WHERE name = %s",
            (photo_path, name)
        )
        print(f"Updated {name} -> {photo_path}")
    
    conn.commit()
    conn.close()
    print("Photo paths updated!")

if __name__ == '__main__':
    fix_photo_paths()
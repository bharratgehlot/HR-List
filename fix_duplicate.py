from postgres_sql import get_connection

def fix_duplicate():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Update the duplicate entry with tab character in name
    cursor.execute(
        "UPDATE contacts SET photo = %s WHERE name LIKE %s",
        ("/uploads/five.jpg", "Rangoli Bhatt%")
    )
    
    conn.commit()
    conn.close()
    print("Fixed duplicate Rangoli Bhatt entry!")

if __name__ == '__main__':
    fix_duplicate()
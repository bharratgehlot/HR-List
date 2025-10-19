from postgres_sql import get_connection

def list_contacts():
    """Show all contacts with their IDs"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, company, email FROM contacts ORDER BY created_at DESC;")
    contacts = cursor.fetchall()
    conn.close()
    
    print("Current contacts:")
    print("-" * 50)
    for contact in contacts:
        print(f"ID: {contact[0]} | {contact[1]} | {contact[2]} | {contact[3]}")
    print(f"\nTotal: {len(contacts)} contacts")

def delete_by_id(contact_id):
    """Delete contact by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    if deleted > 0:
        print(f"Deleted contact with ID {contact_id}")
    else:
        print(f"No contact found with ID {contact_id}")

def delete_by_name(name):
    """Delete contact by name"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name ILIKE %s", (f"%{name}%",))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"Deleted {deleted} contact(s) matching '{name}'")

def delete_all():
    """Delete all contacts"""
    confirm = input("Are you sure you want to delete ALL contacts? (yes/no): ")
    if confirm.lower() == 'yes':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts")
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        print(f"Deleted all {deleted} contacts")
    else:
        print("Operation cancelled")

if __name__ == '__main__':
    print("Database Record Manager")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. List all contacts")
        print("2. Delete by ID")
        print("3. Delete by name")
        print("4. Delete all contacts")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            list_contacts()
        elif choice == '2':
            try:
                contact_id = int(input("Enter contact ID to delete: "))
                delete_by_id(contact_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            name = input("Enter name to delete: ").strip()
            if name:
                delete_by_name(name)
            else:
                print("Name cannot be empty")
        elif choice == '4':
            delete_all()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

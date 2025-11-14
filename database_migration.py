import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import json

load_dotenv()

def get_source_connection():
    """Connect to source database"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

def get_target_connection(target_url):
    """Connect to target database"""
    return psycopg2.connect(target_url, cursor_factory=RealDictCursor)

def migrate_database(target_database_url):
    """Migrate entire database to target"""
    try:
        print("🔄 Starting database migration...")
        
        # Connect to both databases
        source_conn = get_source_connection()
        target_conn = get_target_connection(target_database_url)
        
        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()
        
        # 1. Create table structure in target
        print("📋 Creating table structure...")
        target_cursor.execute("""
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
        
        # 2. Copy all data
        print("📊 Copying data...")
        source_cursor.execute("SELECT * FROM contacts ORDER BY id")
        contacts = source_cursor.fetchall()
        
        for contact in contacts:
            target_cursor.execute("""
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
        
        target_conn.commit()
        
        # Verify migration
        target_cursor.execute("SELECT COUNT(*) FROM contacts")
        target_count = target_cursor.fetchone()['count']
        
        source_cursor.execute("SELECT COUNT(*) FROM contacts")
        source_count = source_cursor.fetchone()['count']
        
        print(f"✅ Migration completed!")
        print(f"   Source records: {source_count}")
        print(f"   Target records: {target_count}")
        
        source_conn.close()
        target_conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def export_to_csv():
    """Export data to CSV for easy transfer"""
    try:
        import csv
        
        conn = get_source_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM contacts ORDER BY id")
        contacts = cursor.fetchall()
        
        # Export to CSV
        with open('contacts_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
            if contacts:
                fieldnames = contacts[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for contact in contacts:
                    writer.writerow(dict(contact))
        
        conn.close()
        print(f"✅ Data exported to contacts_export.csv ({len(contacts)} records)")
        return True
        
    except Exception as e:
        print(f"❌ CSV export failed: {e}")
        return False

def import_from_csv(target_database_url, csv_file='contacts_export.csv'):
    """Import data from CSV to target database"""
    try:
        import csv
        
        conn = get_target_connection(target_database_url)
        cursor = conn.cursor()
        
        # Create table
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
        
        # Import data
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                cursor.execute("""
                    INSERT INTO contacts (photo, name, company, location, position, number, email, status, url, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['photo'] if row['photo'] else None,
                    row['name'],
                    row['company'],
                    row['location'],
                    row['position'] if row['position'] else None,
                    row['number'],
                    row['email'],
                    row['status'],
                    row['url'] if row['url'] else None,
                    row['created_at']
                ))
                count += 1
        
        conn.commit()
        conn.close()
        print(f"✅ Imported {count} records from CSV")
        return True
        
    except Exception as e:
        print(f"❌ CSV import failed: {e}")
        return False

if __name__ == '__main__':
    print("Database Migration Tool")
    print("======================")
    print("1. Direct migration (database to database)")
    print("2. Export to CSV")
    print("3. Import from CSV")
    
    choice = input("Choose option (1-3): ")
    
    if choice == '1':
        target_url = input("Enter target database URL: ")
        migrate_database(target_url)
    elif choice == '2':
        export_to_csv()
    elif choice == '3':
        target_url = input("Enter target database URL: ")
        csv_file = input("Enter CSV file path (or press Enter for 'contacts_export.csv'): ")
        if not csv_file:
            csv_file = 'contacts_export.csv'
        import_from_csv(target_url, csv_file)
    else:
        print("Invalid choice")
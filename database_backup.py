import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

def backup_database_structure():
    """Export database schema/structure"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get table structure
        cursor.execute("""
            SELECT 
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        # Get constraints and indexes
        cursor.execute("""
            SELECT 
                tc.table_name,
                tc.constraint_name,
                tc.constraint_type,
                kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_schema = 'public'
        """)
        
        constraints = cursor.fetchall()
        
        # Generate CREATE TABLE statements
        tables = {}
        for col in columns:
            table_name = col['table_name']
            if table_name not in tables:
                tables[table_name] = []
            
            col_def = f"{col['column_name']} {col['data_type']}"
            if col['character_maximum_length']:
                col_def += f"({col['character_maximum_length']})"
            if col['is_nullable'] == 'NO':
                col_def += " NOT NULL"
            if col['column_default']:
                col_def += f" DEFAULT {col['column_default']}"
            
            tables[table_name].append(col_def)
        
        # Create schema backup file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        schema_file = f"backup_schema_{timestamp}.sql"
        
        with open(schema_file, 'w') as f:
            f.write("-- Database Schema Backup\n")
            f.write(f"-- Generated on: {datetime.now()}\n\n")
            
            for table_name, columns in tables.items():
                f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
                f.write(",\n".join([f"    {col}" for col in columns]))
                
                # Add constraints
                table_constraints = [c for c in constraints if c['table_name'] == table_name]
                for constraint in table_constraints:
                    if constraint['constraint_type'] == 'PRIMARY KEY':
                        f.write(f",\n    PRIMARY KEY ({constraint['column_name']})")
                
                f.write("\n);\n\n")
        
        conn.close()
        print(f"✅ Schema backup created: {schema_file}")
        return schema_file
        
    except Exception as e:
        print(f"❌ Schema backup failed: {e}")
        return None

def backup_database_data():
    """Export all data from database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create data backup files
        data_sql_file = f"backup_data_{timestamp}.sql"
        data_json_file = f"backup_data_{timestamp}.json"
        
        all_data = {}
        
        with open(data_sql_file, 'w') as sql_file:
            sql_file.write("-- Database Data Backup\n")
            sql_file.write(f"-- Generated on: {datetime.now()}\n\n")
            
            for table in tables:
                table_name = table['table_name']
                
                # Get all data from table
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if rows:
                    # Convert to regular dict for JSON serialization
                    table_data = [dict(row) for row in rows]
                    all_data[table_name] = table_data
                    
                    # Generate INSERT statements
                    sql_file.write(f"-- Data for table: {table_name}\n")
                    
                    for row in rows:
                        columns = list(row.keys())
                        values = []
                        
                        for value in row.values():
                            if value is None:
                                values.append("NULL")
                            elif isinstance(value, str):
                                # Escape single quotes
                                escaped_value = value.replace("'", "''")
                                values.append(f"'{escaped_value}'")
                            elif isinstance(value, datetime):
                                values.append(f"'{value}'")
                            else:
                                values.append(str(value))
                        
                        sql_file.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n")
                    
                    sql_file.write("\n")
        
        # Save as JSON for easy data manipulation
        with open(data_json_file, 'w') as json_file:
            json.dump(all_data, json_file, indent=2, default=str)
        
        conn.close()
        print(f"✅ Data backup created: {data_sql_file}")
        print(f"✅ JSON backup created: {data_json_file}")
        return data_sql_file, data_json_file
        
    except Exception as e:
        print(f"❌ Data backup failed: {e}")
        return None, None

def create_restore_script():
    """Create a script to restore the database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    restore_file = f"restore_database_{timestamp}.py"
    
    restore_script = '''import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def restore_database(schema_file, data_file):
    """Restore database from backup files"""
    try:
        # Connect to target database
        database_url = os.getenv('DATABASE_URL')  # or set your target database URL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🔄 Restoring database schema...")
        # Execute schema file
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
            cursor.execute(schema_sql)
        
        print("🔄 Restoring database data...")
        # Execute data file
        with open(data_file, 'r') as f:
            data_sql = f.read()
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in data_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
            for statement in statements:
                if statement:
                    cursor.execute(statement)
        
        conn.commit()
        conn.close()
        print("✅ Database restored successfully!")
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")

if __name__ == '__main__':
    # Update these filenames with your actual backup files
    schema_file = "backup_schema_YYYYMMDD_HHMMSS.sql"
    data_file = "backup_data_YYYYMMDD_HHMMSS.sql"
    
    restore_database(schema_file, data_file)
'''
    
    with open(restore_file, 'w') as f:
        f.write(restore_script)
    
    print(f"✅ Restore script created: {restore_file}")
    return restore_file

def full_backup():
    """Perform complete database backup"""
    print("🚀 Starting full database backup...")
    
    # Create backup directory
    backup_dir = f"database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Change to backup directory
    original_dir = os.getcwd()
    os.chdir(backup_dir)
    
    try:
        # Backup schema
        schema_file = backup_database_structure()
        
        # Backup data
        data_sql_file, data_json_file = backup_database_data()
        
        # Create restore script
        restore_file = create_restore_script()
        
        # Create README
        with open("README.txt", 'w') as f:
            f.write("Database Backup Files\n")
            f.write("====================\n\n")
            f.write(f"Backup created on: {datetime.now()}\n\n")
            f.write("Files included:\n")
            if schema_file:
                f.write(f"- {schema_file}: Database structure/schema\n")
            if data_sql_file:
                f.write(f"- {data_sql_file}: Data in SQL format\n")
            if data_json_file:
                f.write(f"- {data_json_file}: Data in JSON format\n")
            if restore_file:
                f.write(f"- {restore_file}: Restoration script\n")
            f.write("\nTo restore:\n")
            f.write("1. Update DATABASE_URL in .env file\n")
            f.write(f"2. Run: python {restore_file}\n")
        
        os.chdir(original_dir)
        print(f"\n✅ Complete backup created in directory: {backup_dir}")
        
    except Exception as e:
        os.chdir(original_dir)
        print(f"❌ Backup failed: {e}")

if __name__ == '__main__':
    full_backup()
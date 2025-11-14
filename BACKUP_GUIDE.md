# Database Backup & Migration Guide

## Quick Start

### 1. Complete Backup (Recommended)
```bash
python database_backup.py
```
This creates a timestamped folder with:
- Schema backup (SQL)
- Data backup (SQL + JSON)
- Restore script
- README with instructions

### 2. Database Migration
```bash
python database_migration.py
```
Choose from:
1. **Direct migration** - Copy directly between databases
2. **Export to CSV** - Create portable CSV file
3. **Import from CSV** - Load CSV into new database

## Backup Files Created

### Schema Backup (`backup_schema_YYYYMMDD_HHMMSS.sql`)
- Complete table structure
- Column definitions
- Constraints and indexes
- Ready for CREATE TABLE commands

### Data Backup (`backup_data_YYYYMMDD_HHMMSS.sql`)
- All INSERT statements
- Complete data export
- Ready to execute on new database

### JSON Backup (`backup_data_YYYYMMDD_HHMMSS.json`)
- Human-readable format
- Easy data manipulation
- Programming-friendly structure

## Usage Examples

### Backup Current Database
```python
from database_backup import full_backup
full_backup()
```

### Migrate to New Database
```python
from database_migration import migrate_database
target_url = "postgresql://user:pass@host:port/newdb"
migrate_database(target_url)
```

### Export/Import via CSV
```python
from database_migration import export_to_csv, import_from_csv

# Export
export_to_csv()

# Import to new database
target_url = "postgresql://user:pass@host:port/newdb"
import_from_csv(target_url, 'contacts_export.csv')
```

## Restore Process

1. Set up new database
2. Update `.env` with new `DATABASE_URL`
3. Run the generated restore script:
   ```bash
   python restore_database_YYYYMMDD_HHMMSS.py
   ```

## Notes

- All scripts use your existing `.env` configuration
- Backups include timestamps to avoid conflicts
- CSV export handles special characters and NULL values
- Direct migration preserves all data types and timestamps
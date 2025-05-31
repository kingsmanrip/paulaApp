#!/usr/bin/env python3
import os
import shutil
import sqlite3
from datetime import datetime

def backup_database():
    # Source database path
    source_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'employee_tracker.db')
    
    # Create backup directory if it doesn't exist
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_save_folder')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate timestamp for the backup file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f"employee_tracker_backup_{timestamp}.db")
    
    # Check if the source database exists
    if not os.path.exists(source_db):
        print(f"Error: Source database not found at {source_db}")
        return False
    
    try:
        # Create a connection to ensure the database is valid
        conn = sqlite3.connect(source_db)
        conn.close()
        
        # Copy the database file
        shutil.copy2(source_db, backup_file)
        
        print(f"Database backup created successfully: {backup_file}")
        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

if __name__ == "__main__":
    backup_database()

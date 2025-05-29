#!/usr/bin/env python3
import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'employee_tracker.db')

def assign_secretary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Assigning Fatima Gonzalez as secretary to Employee2...")
    
    # Rename Employee2 squad to indicate it's for the secretary
    cursor.execute("""
        UPDATE squad 
        SET name = 'Employee2 - Secretary (601-610-2935)' 
        WHERE id = 2
    """)
    
    # Assign Fatima to Employee2
    cursor.execute("""
        UPDATE employee 
        SET squad_id = 2 
        WHERE name = 'Fatima Gonzalez'
    """)
    
    # Verify the changes
    cursor.execute("""
        SELECT e.name, s.name 
        FROM employee e 
        JOIN squad s ON e.squad_id = s.id 
        WHERE e.name = 'Fatima Gonzalez'
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"Successfully assigned {result[0]} to {result[1]}")
    else:
        print("Assignment failed")
    
    # Commit all changes
    conn.commit()
    conn.close()

if __name__ == "__main__":
    assign_secretary()

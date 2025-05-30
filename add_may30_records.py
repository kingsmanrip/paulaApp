#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'employee_tracker.db')

# Define time record data for May 30, 2025
time_records = [
    # Team 1: Joseph Mcswain's team
    {"name": "Joseph Mcswain", "clock_in": "2025-05-30 07:18:00", "location_in": "908 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:09:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39301"},
    {"name": "Jorge Rodas", "clock_in": "2025-05-30 07:18:00", "location_in": "908 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:09:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39301"},
    {"name": "Daniel Velez", "clock_in": "2025-05-30 07:18:00", "location_in": "908 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:09:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39301"},
    {"name": "Carlos Guevara", "clock_in": "2025-05-30 07:18:00", "location_in": "908 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:09:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39301"},
    {"name": "Luis Amador", "clock_in": "2025-05-30 07:18:00", "location_in": "908 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:09:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39301"},
    {"name": "Julio Funes", "clock_in": "2025-05-30 07:18:00", "location_in": "908 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:09:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39301"},
     
    # Team 2: Taiwan Brown's team
    {"name": "Taiwan Brown", "clock_in": "2025-05-30 07:41:00", "location_in": "1424 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:07:00", "location_out": "2590 Sellers Dr, Meridian MS 39301"},
    {"name": "Oscar Hernandez", "clock_in": "2025-05-30 07:41:00", "location_in": "1424 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:07:00", "location_out": "2590 Sellers Dr, Meridian MS 39301"},
    {"name": "Luis Velasquez", "clock_in": "2025-05-30 07:41:00", "location_in": "1424 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:07:00", "location_out": "2590 Sellers Dr, Meridian MS 39301"},
    {"name": "Hector Hernandez", "clock_in": "2025-05-30 07:41:00", "location_in": "1424 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:07:00", "location_out": "2590 Sellers Dr, Meridian MS 39301"},
    {"name": "Ignacio Antonio", "clock_in": "2025-05-30 07:41:00", "location_in": "1424 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:07:00", "location_out": "2590 Sellers Dr, Meridian MS 39301"},
    {"name": "Jaime Garcia", "clock_in": "2025-05-30 07:41:00", "location_in": "1424 29th Ave, Meridian MS 39301", 
     "clock_out": "2025-05-30 14:07:00", "location_out": "2590 Sellers Dr, Meridian MS 39301"},
    
    # Team 3: Caleb Bryant's team
    {"name": "Caleb Bryant", "clock_in": "2025-05-30 08:02:00", "location_in": "625 Magnolia Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 12:27:00", "location_out": "525 Elm Ave NW, Magee MS 39111"},
    {"name": "Aaron Mitchell", "clock_in": "2025-05-30 08:02:00", "location_in": "625 Magnolia Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 12:27:00", "location_out": "525 Elm Ave NW, Magee MS 39111"},
    {"name": "Seth James", "clock_in": "2025-05-30 08:02:00", "location_in": "625 Magnolia Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 12:27:00", "location_out": "525 Elm Ave NW, Magee MS 39111"},
    {"name": "Colton Poore", "clock_in": "2025-05-30 08:02:00", "location_in": "625 Magnolia Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 12:27:00", "location_out": "525 Elm Ave NW, Magee MS 39111"},
    {"name": "David Pool", "clock_in": "2025-05-30 08:02:00", "location_in": "625 Magnolia Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 12:27:00", "location_out": "525 Elm Ave NW, Magee MS 39111"},
    {"name": "Shawn Beard", "clock_in": "2025-05-30 08:02:00", "location_in": "625 Magnolia Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 12:27:00", "location_out": "525 Elm Ave NW, Magee MS 39111"},
    
    # Team 4: Cristian Pérez's team - Note Antonio Jimenez clocked in but not out
    {"name": "Cristian Pérez", "clock_in": "2025-05-30 08:40:00", "location_in": "109 W Pike St, Osyka MS 39657", 
     "clock_out": "2025-05-30 13:42:00", "location_out": "1106 Second St N, Osyka MS 39667"},
    {"name": "Yovanis Diaz", "clock_in": "2025-05-30 08:40:00", "location_in": "109 W Pike St, Osyka MS 39657", 
     "clock_out": "2025-05-30 13:42:00", "location_out": "1106 Second St N, Osyka MS 39667"},
    {"name": "Willy Galvez", "clock_in": "2025-05-30 08:40:00", "location_in": "109 W Pike St, Osyka MS 39657", 
     "clock_out": "2025-05-30 13:42:00", "location_out": "1106 Second St N, Osyka MS 39667"},
    {"name": "Eliseo Galvez", "clock_in": "2025-05-30 08:40:00", "location_in": "109 W Pike St, Osyka MS 39657", 
     "clock_out": "2025-05-30 13:42:00", "location_out": "1106 Second St N, Osyka MS 39667"},
    {"name": "Reynaldo Martinez", "clock_in": "2025-05-30 08:40:00", "location_in": "109 W Pike St, Osyka MS 39657", 
     "clock_out": "2025-05-30 13:42:00", "location_out": "1106 Second St N, Osyka MS 39667"},
    {"name": "Antonio Jimenez", "clock_in": "2025-05-30 08:40:00", "location_in": "109 W Pike St, Osyka MS 39657", 
     "clock_out": None, "location_out": None},  # No clock-out record
    
    # Team 5: Johnnie Roberts' team
    {"name": "Jeramy Smith", "clock_in": "2025-05-30 09:02:00", "location_in": "618 Elm Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 14:28:00", "location_out": "601 Cherry St NW, Magee MS 39111"},
    {"name": "Johnnie Roberts", "clock_in": "2025-05-30 09:02:00", "location_in": "618 Elm Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 14:28:00", "location_out": "601 Cherry St NW, Magee MS 39111"},
    {"name": "Blake Hay", "clock_in": "2025-05-30 09:02:00", "location_in": "618 Elm Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 14:28:00", "location_out": "601 Cherry St NW, Magee MS 39111"},
    {"name": "Maurilio Galvez", "clock_in": "2025-05-30 09:02:00", "location_in": "618 Elm Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 14:28:00", "location_out": "601 Cherry St NW, Magee MS 39111"},
    {"name": "Rodolfo Coronado", "clock_in": "2025-05-30 09:02:00", "location_in": "618 Elm Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-30 14:28:00", "location_out": "601 Cherry St NW, Magee MS 39111"},
    
    # Team 6: James Jarrell's team
    {"name": "James Jarrell", "clock_in": "2025-05-30 09:15:00", "location_in": "E Gardens Dr, Meridian MS 39301", 
     "clock_out": "2025-05-30 13:01:00", "location_out": "I-20 W, Meridian MS 39301"},
    {"name": "Thomas King", "clock_in": "2025-05-30 09:15:00", "location_in": "E Gardens Dr, Meridian MS 39301", 
     "clock_out": "2025-05-30 13:01:00", "location_out": "I-20 W, Meridian MS 39301"},
    {"name": "Seth Pope", "clock_in": "2025-05-30 09:15:00", "location_in": "E Gardens Dr, Meridian MS 39301", 
     "clock_out": "2025-05-30 13:01:00", "location_out": "I-20 W, Meridian MS 39301"},
    {"name": "Kyzer Revette", "clock_in": "2025-05-30 09:15:00", "location_in": "E Gardens Dr, Meridian MS 39301", 
     "clock_out": "2025-05-30 13:01:00", "location_out": "I-20 W, Meridian MS 39301"},
    {"name": "Richard Carter", "clock_in": "2025-05-30 09:15:00", "location_in": "E Gardens Dr, Meridian MS 39301", 
     "clock_out": "2025-05-30 13:01:00", "location_out": "I-20 W, Meridian MS 39301"}
]

def add_time_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Adding {len(time_records)} time records for May 30, 2025...")
    
    # Create a dictionary of employees by name for quick lookup
    cursor.execute("SELECT id, name FROM employee")
    employees = {name: id for id, name in cursor.fetchall()}
    
    # Track statistics
    processed = 0
    skipped = 0
    errors = 0
    
    # Process each time record
    for record in time_records:
        try:
            # Find employee by name
            employee_id = employees.get(record["name"])
            if not employee_id:
                print(f"Error: Employee not found: {record['name']}")
                errors += 1
                continue
                
            # Check if record already exists for this day and employee
            cursor.execute("""
                SELECT COUNT(*) FROM time_record 
                WHERE employee_id = ? AND DATE(clock_in) = DATE(?)
            """, (employee_id, record["clock_in"]))
            
            if cursor.fetchone()[0] > 0:
                print(f"Skipping duplicate record for {record['name']} on 2025-05-30")
                skipped += 1
                continue
                
            # Insert time record
            cursor.execute("""
                INSERT INTO time_record (employee_id, clock_in, clock_out, location_in, location_out)
                VALUES (?, ?, ?, ?, ?)
            """, (
                employee_id,
                record["clock_in"],
                record["clock_out"],  # This will be NULL for Antonio Jimenez
                record["location_in"],
                record["location_out"]  # This will be NULL for Antonio Jimenez
            ))
            
            processed += 1
            if record["clock_out"]:
                print(f"Added complete record for {record['name']} on 2025-05-30")
            else:
                print(f"Added clock-in only record for {record['name']} on 2025-05-30 (no clock-out)")
            
        except Exception as e:
            print(f"Error processing record for {record['name']}: {str(e)}")
            errors += 1
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    print(f"Records processed: {processed}")
    print(f"Records skipped: {skipped}")
    print(f"Errors: {errors}")
    
    return processed, skipped, errors

if __name__ == "__main__":
    add_time_records()

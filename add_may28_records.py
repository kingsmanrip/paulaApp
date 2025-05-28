#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'employee_tracker.db')

# Define time record data for May 28, 2025
time_records = [
    # 1. Team 1: Taiwan Brown's team in Meridian MS
    {"name": "Taiwan Brown", "clock_in": "2025-05-28 07:21:00", "location_in": "2719 40th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:31:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39307"},
    {"name": "Oscar Hernandez", "clock_in": "2025-05-28 07:21:00", "location_in": "2719 40th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:31:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39307"},
    {"name": "Luis Velasquez", "clock_in": "2025-05-28 07:21:00", "location_in": "2719 40th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:31:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39307"},
    {"name": "Hector Hernandez", "clock_in": "2025-05-28 07:21:00", "location_in": "2719 40th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:31:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39307"},
    {"name": "Ignacio Antonio", "clock_in": "2025-05-28 07:21:00", "location_in": "2719 40th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:31:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39307"},
    {"name": "Jaime Garcia", "clock_in": "2025-05-28 07:21:00", "location_in": "2719 40th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:31:00", "location_out": "Martin Luther King Jr Memorial Dr, Meridian MS 39307"},
     
    # 2. Team 2: Cristian Pérez's team in Osyka MS
    {"name": "Cristian Pérez", "clock_in": "2025-05-28 08:25:00", "location_in": "1042 Second St S, Osyka MS 39657", 
     "clock_out": "2025-05-28 16:35:00", "location_out": "1091 Second St S, Osyka MS 39657"},
    {"name": "Yovanis Diaz", "clock_in": "2025-05-28 08:25:00", "location_in": "1042 Second St S, Osyka MS 39657", 
     "clock_out": "2025-05-28 16:35:00", "location_out": "1091 Second St S, Osyka MS 39657"},
    {"name": "Willy Galvez", "clock_in": "2025-05-28 08:25:00", "location_in": "1042 Second St S, Osyka MS 39657", 
     "clock_out": "2025-05-28 16:35:00", "location_out": "1091 Second St S, Osyka MS 39657"},
    {"name": "Eliseo Galvez", "clock_in": "2025-05-28 08:25:00", "location_in": "1042 Second St S, Osyka MS 39657", 
     "clock_out": "2025-05-28 16:35:00", "location_out": "1091 Second St S, Osyka MS 39657"},
    {"name": "Antonio Jimenez", "clock_in": "2025-05-28 08:25:00", "location_in": "1042 Second St S, Osyka MS 39657", 
     "clock_out": "2025-05-28 16:35:00", "location_out": "1091 Second St S, Osyka MS 39657"},
    {"name": "Reynaldo Martinez", "clock_in": "2025-05-28 08:25:00", "location_in": "1042 Second St S, Osyka MS 39657", 
     "clock_out": "2025-05-28 16:35:00", "location_out": "1091 Second St S, Osyka MS 39657"},
    
    # 3. Team 3: Johnnie Roberts' team in Magee MS
    {"name": "Johnnie Roberts", "clock_in": "2025-05-28 08:29:00", "location_in": "358–360 Sixth St SE, Magee MS 39111", 
     "clock_out": "2025-05-28 16:31:00", "location_out": "600–608 Elm Ave NW, Magee MS 39111"},
    {"name": "Blake Hay", "clock_in": "2025-05-28 08:29:00", "location_in": "358–360 Sixth St SE, Magee MS 39111", 
     "clock_out": "2025-05-28 16:31:00", "location_out": "600–608 Elm Ave NW, Magee MS 39111"},
    {"name": "Maurilio Galvez", "clock_in": "2025-05-28 08:29:00", "location_in": "358–360 Sixth St SE, Magee MS 39111", 
     "clock_out": "2025-05-28 16:31:00", "location_out": "600–608 Elm Ave NW, Magee MS 39111"},
    {"name": "Rodolfo Coronado", "clock_in": "2025-05-28 08:29:00", "location_in": "358–360 Sixth St SE, Magee MS 39111", 
     "clock_out": "2025-05-28 16:31:00", "location_out": "600–608 Elm Ave NW, Magee MS 39111"},
    
    # 4. Team 4: Joseph Mcswain's team in Meridian MS
    {"name": "Joseph Mcswain", "clock_in": "2025-05-28 08:36:00", "location_in": "1020 34th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:27:00", "location_out": "Old 31st Ave S, Meridian MS 39307"},
    {"name": "Jorge Rodas", "clock_in": "2025-05-28 08:36:00", "location_in": "1020 34th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:27:00", "location_out": "Old 31st Ave S, Meridian MS 39307"},
    {"name": "Daniel Velez", "clock_in": "2025-05-28 08:36:00", "location_in": "1020 34th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:27:00", "location_out": "Old 31st Ave S, Meridian MS 39307"},
    {"name": "Carlos Guevara", "clock_in": "2025-05-28 08:36:00", "location_in": "1020 34th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:27:00", "location_out": "Old 31st Ave S, Meridian MS 39307"},
    {"name": "Luis Amador", "clock_in": "2025-05-28 08:36:00", "location_in": "1020 34th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:27:00", "location_out": "Old 31st Ave S, Meridian MS 39307"},
    {"name": "Julio Funes", "clock_in": "2025-05-28 08:36:00", "location_in": "1020 34th St, Meridian MS 39305", 
     "clock_out": "2025-05-28 15:27:00", "location_out": "Old 31st Ave S, Meridian MS 39307"},
    
    # 5. Team 5: Caleb Bryant's team in Magee MS
    {"name": "Caleb Bryant", "clock_in": "2025-05-28 08:38:00", "location_in": "607 Ninth Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-28 16:47:00", "location_out": "600–674 Magnolia Ave NW, Magee MS 39111"},
    {"name": "Aaron Mitchell", "clock_in": "2025-05-28 08:38:00", "location_in": "607 Ninth Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-28 16:47:00", "location_out": "600–674 Magnolia Ave NW, Magee MS 39111"},
    {"name": "Seth James", "clock_in": "2025-05-28 08:38:00", "location_in": "607 Ninth Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-28 16:47:00", "location_out": "600–674 Magnolia Ave NW, Magee MS 39111"},
    {"name": "Colton Poore", "clock_in": "2025-05-28 08:38:00", "location_in": "607 Ninth Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-28 16:47:00", "location_out": "600–674 Magnolia Ave NW, Magee MS 39111"},
    {"name": "David Pool", "clock_in": "2025-05-28 08:38:00", "location_in": "607 Ninth Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-28 16:47:00", "location_out": "600–674 Magnolia Ave NW, Magee MS 39111"},
    {"name": "Shawn Beard", "clock_in": "2025-05-28 08:38:00", "location_in": "607 Ninth Ave NW, Magee MS 39111", 
     "clock_out": "2025-05-28 16:47:00", "location_out": "600–674 Magnolia Ave NW, Magee MS 39111"},
    
    # 6. Team 6: James Jarrell's team in Marion MS - Different clock-out times for team members
    {"name": "James Jarrell", "clock_in": "2025-05-28 09:53:00", "location_in": "4858 Marion Dr, Marion MS 39342", 
     "clock_out": "2025-05-28 13:07:00", "location_out": "736 Alamutcha St, Marion MS 39342"},
    {"name": "Thomas King", "clock_in": "2025-05-28 09:53:00", "location_in": "4858 Marion Dr, Marion MS 39342", 
     "clock_out": "2025-05-28 13:07:00", "location_out": "736 Alamutcha St, Marion MS 39342"},
    {"name": "Seth Pope", "clock_in": "2025-05-28 09:53:00", "location_in": "4858 Marion Dr, Marion MS 39342", 
     "clock_out": "2025-05-28 11:20:00", "location_out": "1414 Rubush Ave, Meridian MS 39301"},
    {"name": "Kyzer Revette", "clock_in": "2025-05-28 09:53:00", "location_in": "4858 Marion Dr, Marion MS 39342", 
     "clock_out": "2025-05-28 11:20:00", "location_out": "1414 Rubush Ave, Meridian MS 39301"},
    {"name": "Richard Carter", "clock_in": "2025-05-28 09:53:00", "location_in": "4858 Marion Dr, Marion MS 39342", 
     "clock_out": "2025-05-28 11:20:00", "location_out": "1414 Rubush Ave, Meridian MS 39301"}
]

def add_time_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Adding {len(time_records)} time records for May 28, 2025...")
    
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
                print(f"Skipping duplicate record for {record['name']} on 2025-05-28")
                skipped += 1
                continue
                
            # Insert time record
            cursor.execute("""
                INSERT INTO time_record (employee_id, clock_in, clock_out, location_in, location_out)
                VALUES (?, ?, ?, ?, ?)
            """, (
                employee_id,
                record["clock_in"],
                record["clock_out"],
                record["location_in"],
                record["location_out"]
            ))
            
            processed += 1
            print(f"Added record for {record['name']} on 2025-05-28")
            
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

#!/usr/bin/env python3
import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'employee_tracker.db')

# New squad assignments - only for employees without current assignments
squad_assignments = {
    # Employee3 squad
    "Employee3": [
        "James Jarrell",
        "Thomas King",
        "Seth Pope",
        "Kyzer Revette",
        "Richard Carter"
    ],
    # Employee4 squad
    "Employee4": [
        "Joseph Mcswain",
        "Jorge Rodas",
        "Daniel Velez",
        "Carlos Guevara",
        "Luis Amador",
        "Julio Funes"
    ],
    # Employee5 squad
    "Employee5": [
        "Taiwan Brown",
        "Oscar Hernandez",
        "Luis Velasquez",
        "Hector Hernandez",
        "Ignacio Antonio"
        # Note: Jaime Garcia stays in Employee7 per existing assignment
    ],
    # Employee7 squad - add only those not already assigned
    "Employee7": [
        "Cristian Pérez",
        "Yovanis Diaz",
        "Eliseo Galvez"
        # Note: Willy Galvez, Antonio Jimenez, Reynaldo Martinez already in this squad
    ],
    # Employee8 squad - add only those not already assigned
    "Employee8": [
        "Rodolfo Coronado"
        # Note: Johnnie Roberts, Blake Hay, Maurilio Galvez already in this squad
    ]
}

def update_squad_assignments():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Updating squad assignments for unassigned employees...")
    
    # Get squad IDs
    cursor.execute("SELECT id, name FROM squad")
    squads = {name.split(' ')[0]: id for id, name in cursor.fetchall()}
    
    # Get all employees
    cursor.execute("SELECT id, name, squad_id FROM employee")
    employees = {name: (id, squad_id) for id, name, squad_id in cursor.fetchall()}
    
    # Track statistics
    updated = 0
    skipped = 0
    errors = 0
    
    # Process each squad assignment
    for squad_name, employee_list in squad_assignments.items():
        squad_id = squads.get(squad_name)
        if not squad_id:
            print(f"Error: Squad not found: {squad_name}")
            errors += 1
            continue
            
        for employee_name in employee_list:
            try:
                if employee_name not in employees:
                    print(f"Error: Employee not found: {employee_name}")
                    errors += 1
                    continue
                    
                employee_id, current_squad_id = employees[employee_name]
                
                # Skip if employee already has a squad
                if current_squad_id is not None:
                    print(f"Skipping {employee_name} - already assigned to squad {current_squad_id}")
                    skipped += 1
                    continue
                
                # Update squad assignment
                cursor.execute("UPDATE employee SET squad_id = ? WHERE id = ?", (squad_id, employee_id))
                updated += 1
                print(f"Assigned {employee_name} to {squad_name}")
                
            except Exception as e:
                print(f"Error processing {employee_name}: {str(e)}")
                errors += 1
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    print(f"Squad assignments updated: {updated}")
    print(f"Employees skipped (already assigned): {skipped}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    update_squad_assignments()

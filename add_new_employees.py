#!/usr/bin/env python3
from app import app, db, Employee, Squad

def add_missing_employees():
    with app.app_context():
        # Find the appropriate squad (Johnnie Roberts' squad)
        # Since these employees worked with Johnnie Roberts, they likely belong to the same squad
        johnnie = Employee.query.filter(Employee.name.ilike('%johnnie roberts%')).first()
        squad_id = johnnie.squad_id if johnnie else None
        
        # Create the new employees
        new_employees = [
            {
                "name": "Jeremy Smith",
                "squad_id": squad_id
            },
            {
                "name": "Detrick Conerly",
                "squad_id": squad_id
            }
        ]
        
        for emp_data in new_employees:
            # Check if employee already exists
            existing = Employee.query.filter(Employee.name == emp_data["name"]).first()
            if existing:
                print(f"Employee {emp_data['name']} already exists, skipping.")
                continue
                
            # Create new employee
            new_employee = Employee(
                name=emp_data["name"],
                squad_id=emp_data["squad_id"]
            )
            db.session.add(new_employee)
            print(f"Added new employee: {emp_data['name']}")
        
        db.session.commit()
        print("New employees added successfully!")

if __name__ == "__main__":
    add_missing_employees()

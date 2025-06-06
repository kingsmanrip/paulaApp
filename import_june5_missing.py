#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime

def add_missing_employee_records():
    with app.app_context():
        # Get the two new employees
        jeremy = Employee.query.filter(Employee.name == "Jeremy Smith").first()
        detrick = Employee.query.filter(Employee.name == "Detrick Conerly").first()
        
        if not jeremy or not detrick:
            print("Error: Cannot find one or both of the newly added employees")
            return
        
        # Add time records for Johnnie Roberts' team (new employees only)
        clock_in = datetime(2025, 6, 5, 9, 56)
        clock_out = datetime(2025, 6, 5, 15, 58)
        location_in = "1106 Second St N Osyka MS 39667"
        location_out = "US-98 E Tylertown MS 39667"
        
        new_records = []
        
        # Create time record for Jeremy Smith
        jeremy_record = TimeRecord(
            employee_id=jeremy.id,
            clock_in=clock_in,
            clock_out=clock_out,
            location_in=location_in,
            location_out=location_out
        )
        new_records.append(jeremy_record)
        
        # Create time record for Detrick Conerly
        detrick_record = TimeRecord(
            employee_id=detrick.id,
            clock_in=clock_in,
            clock_out=clock_out,
            location_in=location_in,
            location_out=location_out
        )
        new_records.append(detrick_record)
        
        # Add and commit all records
        for record in new_records:
            db.session.add(record)
            
        db.session.commit()
        print(f"Added time records for the 2 new employees")

if __name__ == "__main__":
    add_missing_employee_records()

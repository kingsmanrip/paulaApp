from app import app, db, Employee, TimeRecord
from datetime import datetime

def add_employee8_data():
    with app.app_context():
        # May 21, 2025 data for Employee8 squad
        clock_data = [
            {
                "type": "ClockIn",
                "employees": [
                    "Jeramy Smith",
                    "Johnnie Roberts",
                    "Blake Hay",
                    "Maurilio Galvez"
                ],
                "location": "615–699 Cherry St NW\nMagee MS 39111\nUnited States",
                "date": "May 21, 2025 at 10:18 AM"
            },
            {
                "type": "ClockOut",
                "employees": [
                    "Jeramy Smith",
                    "Johnnie Roberts",
                    "Blake Hay",
                    "Maurilio Galvez"
                ],
                "location": "801–919 Maple Ave NW\nMagee MS 39111\nUnited States",
                "date": "May 21, 2025 at 5:49 PM"
            }
        ]
        
        # Process each record
        for record in clock_data:
            record_type = record["type"]
            employee_list = record["employees"]
            location = record["location"]
            date_str = record["date"]
            
            # Parse date
            try:
                date_obj = datetime.strptime(date_str, '%B %d, %Y at %I:%M %p')
            except ValueError:
                print(f'Error parsing date: {date_str}')
                continue
            
            # Process each employee
            for emp_name in employee_list:
                # Find the employee by exact name match
                employee = Employee.query.filter_by(name=emp_name).first()
                if not employee:
                    # Skip if employee not found
                    print(f"Employee not found: {emp_name}")
                    continue
                
                if record_type == "ClockIn":
                    # Check if there's an existing record for this date
                    start_of_day = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0)
                    end_of_day = datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59)
                    
                    existing_record = TimeRecord.query.filter(
                        TimeRecord.employee_id == employee.id,
                        TimeRecord.clock_in >= start_of_day,
                        TimeRecord.clock_in <= end_of_day
                    ).first()
                    
                    if existing_record:
                        existing_record.clock_in = date_obj
                        existing_record.location_in = location
                        print(f"Updated clock-in for {emp_name} on {date_obj.date()}")
                    else:
                        new_record = TimeRecord(
                            employee_id=employee.id,
                            clock_in=date_obj,
                            location_in=location
                        )
                        db.session.add(new_record)
                        print(f"Added clock-in for {emp_name} on {date_obj.date()}")
                
                elif record_type == "ClockOut":
                    # Find a record for this date without clock-out
                    start_of_day = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0)
                    end_of_day = datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59)
                    
                    existing_record = TimeRecord.query.filter(
                        TimeRecord.employee_id == employee.id,
                        TimeRecord.clock_in >= start_of_day,
                        TimeRecord.clock_in <= end_of_day
                    ).first()
                    
                    if existing_record:
                        existing_record.clock_out = date_obj
                        existing_record.location_out = location
                        print(f"Updated clock-out for {emp_name} on {date_obj.date()}")
                    else:
                        # Create a new record with estimated clock-in
                        new_record = TimeRecord(
                            employee_id=employee.id,
                            clock_in=date_obj.replace(hour=8, minute=0),  # Estimate 8 AM
                            clock_out=date_obj,
                            location_in="Location not recorded",
                            location_out=location
                        )
                        db.session.add(new_record)
                        print(f"Added clock-out (with estimated clock-in) for {emp_name} on {date_obj.date()}")
        
        db.session.commit()
        print("Employee8 squad clock data for May 21, 2025 has been added successfully")

if __name__ == "__main__":
    add_employee8_data()

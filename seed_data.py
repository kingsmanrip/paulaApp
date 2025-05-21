from app import app, db, Employee, TimeRecord, User
from datetime import datetime
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('paula2025*')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        
        # Clear existing data for clean restart
        TimeRecord.query.delete()
        Employee.query.delete()
        db.session.commit()
        
        # List of employees with full names exactly as provided
        employee_names = [
            "James Jarrell",
            "Thomas King", 
            "Seth Pope", 
            "Kyzer Revette", 
            "Joseph Mcswain", 
            "Richard Carter", 
            "Caleb Bryant", 
            "Aaron Mitchell", 
            "Seth James", 
            "Colton Poore", 
            "David Pool",
            "Shawn Beard", 
            "Jeramy Smith", 
            "Johnnie Roberts", 
            "Cristian Pérez", 
            "Taiwan Brown", 
            "Fatima Gonzalez",
            "Juan Pereira", 
            "Yovanis Diaz", 
            "Blake Hay", 
            "Jorge Perez", 
            "Rene Rivas", 
            "Andres Falcon", 
            "Juan Andres Hernandez", 
            "Jorge Rodas", 
            "Daniel Velez",
            "Carlos Guevara", 
            "Luis Amador",
            "Julio Funes",
            "Oscar Hernandez", 
            "Luis Velasquez", 
            "Hector Hernandez",
            "Ignacio Antonio",
            "Jaime Garcia",
            "Willy Galvez", 
            "Eliseo Galvez",
            "Gabriel Garcia", 
            "Antonio Jimenez",
            "Reynaldo Martinez", 
            "Maurilio Galvez", 
            "Rodolfo Coronado"
        ]
        
        # Add employees to the database
        for name in employee_names:
            if not Employee.query.filter_by(name=name).first():
                employee = Employee(name=name)
                db.session.add(employee)
        
        db.session.commit()
        print(f"{len(employee_names)} employees added to database")
        
        # Add clock in/out records exactly as formatted
        clock_records = [
            # May 12, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "Shawn Beard"
            ], 
             "location": "201–299 Dolly Ln NW\nMagee MS 39111\nUnited States", 
             "date": "May 12, 2025 at 9:30 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "Shawn Beard"
            ], 
             "location": "149 Simpson Hwy 149\nMagee MS 39111\nUnited States", 
             "date": "May 12, 2025 at 5:21 PM"},
            
            # May 13, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool"
            ], 
             "location": "203 Fifth Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 13, 2025 at 8:20 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool"
            ], 
             "location": "222 First St NW\nMagee MS 39111\nUnited States", 
             "date": "May 13, 2025 at 4:45 PM"},
            
            # May 14, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "11th Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 14, 2025 at 8:07 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "630 11th Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 14, 2025 at 4:55 PM"},
            
            # May 15, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "201–299 Dolly Ln NW\nMagee MS 39111\nUnited States", 
             "date": "May 15, 2025 at 7:45 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "102 Emily Ln NW\nMagee MS 39111\nUnited States", 
             "date": "May 15, 2025 at 4:36 PM"},
            
            # May 16, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "618 11th Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 16, 2025 at 7:57 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "621 St Louis Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 16, 2025 at 3:07 PM"},
            
            # May 19, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "630 11th Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 19, 2025 at 9:00 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "401–471 NW Rankin\nMagee MS 39111\nUnited States", 
             "date": "May 19, 2025 at 4:12 PM"},
            
            # May 20, 2025
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "603 11th Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 20, 2025 at 7:57 AM"},
            {"type": "ClockOut", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "508 NW Rankin\nMagee MS 39111\nUnited States", 
             "date": "May 20, 2025 at 4:57 PM"},
            
            # May 21, 2025 (Adding today's data)
            {"type": "ClockIn", "employees": [
                "Caleb Bryant", 
                "Aaron Mitchell", 
                "Seth James", 
                "Colton Poore", 
                "David Pool",
                "Shawn Beard"
            ], 
             "location": "603 11th Ave NW\nMagee MS 39111\nUnited States", 
             "date": "May 21, 2025 at 8:00 AM"}
        ]
        
        # Process each record
        for record in clock_records:
            record_type = record["type"]
            employee_list = record["employees"]  # This is now a list of employee names
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
                    else:
                        new_record = TimeRecord(
                            employee_id=employee.id,
                            clock_in=date_obj,
                            location_in=location
                        )
                        db.session.add(new_record)
                
                elif record_type == "ClockOut":
                    # Check for special case of Seth James on May 15 (missing at clock-in)
                    if emp_name == "Seth James" and date_obj.date().day == 15 and date_obj.date().month == 5:
                        # Create a new entry for Seth with estimated clock-in time
                        estimated_clock_in = date_obj.replace(hour=7, minute=45)  # Same time as others
                        new_record = TimeRecord(
                            employee_id=employee.id,
                            clock_in=estimated_clock_in,
                            clock_out=date_obj,
                            location_in=location,  # Use same location
                            location_out=location
                        )
                        db.session.add(new_record)
                        continue
                        
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
        
        db.session.commit()
        print("Clock in/out records added to database")

if __name__ == "__main__":
    seed_database()

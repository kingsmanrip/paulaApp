#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime
import re
from flask import Flask

def parse_date(date_str):
    date_formats = [
        '%b %d, %Y, %I:%M %p',
        '%b %d, %Y, %I:%M %p.',
        '%b %d, %Y, %I:%M%p',
        '%b %d, %Y, %I:%M%p.',
        '%b %d, %Y at %I:%M %p',
        '%B %d, %Y at %I:%M %p',
        '%B %d, %Y, %I:%M %p',
        '%B %d, %Y, %I:%M %p.',
        '%B %d, %Y, %I:%M%p',
        '%B %d, %Y, %I:%M%p.'
    ]
    
    # Normalize format
    date_str = date_str.replace('a.m.', 'AM').replace('p.m.', 'PM')
    date_str = date_str.replace('jun', 'Jun').replace('Jun.', 'Jun')
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    print(f"Failed to parse date: {date_str}")
    return None

def process_bulk_import(data):
    lines = data.strip().split('\n')
    
    current_type = None
    current_employee = None
    current_location = None
    current_date = None
    records = []
    
    for line in lines:
        line = line.strip()
        if not line:
            # Process the collected data if we have a complete record
            if current_type and current_employee and current_location and current_date:
                record = {
                    'type': current_type,
                    'employees': current_employee,
                    'location': current_location,
                    'date': current_date
                }
                records.append(record)
                current_type = None
                current_employee = None
                current_location = None
                current_date = None
            continue
        
        if line.startswith('ClockIn-'):
            current_type = 'ClockIn'
        elif line.startswith('ClockOut-'):
            current_type = 'ClockOut'
        elif line.startswith('employee:'):
            current_employee = line[len('employee:'):].strip()
        elif line.startswith('location:'):
            current_location = line[len('location:'):].strip()
        elif line.startswith('date:'):
            current_date = line[len('date:'):].strip()
    
    # Process the last record if complete
    if current_type and current_employee and current_location and current_date:
        record = {
            'type': current_type,
            'employees': current_employee,
            'location': current_location,
            'date': current_date
        }
        records.append(record)
    
    # Insert the records into the database
    with app.app_context():
        for record in records:
            # Parse the employee names
            employee_names = record['employees'].split('\n')
            if len(employee_names) == 1:
                employee_names = re.split(r',\s*|\s+', record['employees'])
            
            # Clean up names - remove empty strings
            employee_names = [name.strip() for name in employee_names if name.strip()]
            
            # Parse the date
            parsed_date = parse_date(record['date'])
            if not parsed_date:
                print(f"Skipping record due to invalid date: {record['date']}")
                continue
                
            # Process each employee
            for emp_name in employee_names:
                # Find the employee in the database
                employee = Employee.query.filter(Employee.name.ilike(f"%{emp_name}%")).first()
                if not employee:
                    print(f"Employee not found: {emp_name}")
                    continue
                
                # Check if this is a ClockIn or ClockOut
                if record['type'] == 'ClockIn':
                    # Check if a record already exists
                    existing_record = TimeRecord.query.filter_by(
                        employee_id=employee.id,
                        clock_in=parsed_date
                    ).first()
                    
                    if existing_record:
                        print(f"ClockIn record already exists for {emp_name} at {parsed_date}")
                        continue
                    
                    # Create a new record
                    time_record = TimeRecord(
                        employee_id=employee.id,
                        clock_in=parsed_date,
                        location_in=record['location']
                    )
                    db.session.add(time_record)
                    print(f"Added ClockIn for {emp_name} at {parsed_date}")
                    
                elif record['type'] == 'ClockOut':
                    # Find matching ClockIn record
                    matching_record = TimeRecord.query.filter_by(
                        employee_id=employee.id,
                        clock_out=None
                    ).order_by(TimeRecord.clock_in.desc()).first()
                    
                    if matching_record:
                        matching_record.clock_out = parsed_date
                        matching_record.location_out = record['location']
                        print(f"Updated ClockOut for {emp_name} at {parsed_date}")
                    else:
                        # Create a new record with just ClockOut
                        time_record = TimeRecord(
                            employee_id=employee.id,
                            clock_out=parsed_date,
                            location_out=record['location']
                        )
                        db.session.add(time_record)
                        print(f"Added standalone ClockOut for {emp_name} at {parsed_date}")
        
        # Commit the changes
        db.session.commit()
        print("All records imported successfully!")

if __name__ == "__main__":
    with open('june2_records.txt', 'r') as f:
        data = f.read()
    
    process_bulk_import(data)

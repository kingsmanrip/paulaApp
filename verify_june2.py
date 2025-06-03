#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime

with app.app_context():
    # Query for June 2, 2025 records
    june2_start = datetime(2025, 6, 2, 0, 0, 0)
    june2_end = datetime(2025, 6, 3, 0, 0, 0)
    
    records = TimeRecord.query.filter(
        TimeRecord.clock_in >= june2_start,
        TimeRecord.clock_in < june2_end
    ).all()
    
    print(f"Found {len(records)} time records for June 2, 2025")
    
    # Show details of some records
    for i, record in enumerate(records[:5]):  # Show first 5 records
        employee = Employee.query.get(record.employee_id)
        print(f"Record {i+1}: {employee.name} - IN: {record.clock_in} - OUT: {record.clock_out}")

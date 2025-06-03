#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime

with app.app_context():
    # Query for June 3, 2025 records
    june3_start = datetime(2025, 6, 3, 0, 0, 0)
    june3_end = datetime(2025, 6, 4, 0, 0, 0)
    
    records = TimeRecord.query.filter(
        TimeRecord.clock_in >= june3_start,
        TimeRecord.clock_in < june3_end
    ).all()
    
    print(f"Found {len(records)} time records for June 3, 2025")
    
    # Group by team/location
    team_locations = {}
    for record in records:
        employee = Employee.query.get(record.employee_id)
        location = record.location_in.split(',')[0] if record.location_in else "Unknown"
        
        key = location
        if key not in team_locations:
            team_locations[key] = []
        
        team_locations[key].append({
            "name": employee.name,
            "clock_in": record.clock_in,
            "clock_out": record.clock_out,
            "hours": round((record.clock_out - record.clock_in).total_seconds() / 3600, 2) if record.clock_out else 0
        })
    
    # Display team activity
    print("\nJune 3, 2025 Team Activity:")
    print("--------------------------")
    for location, employees in team_locations.items():
        print(f"\n{location} - {len(employees)} employees")
        clock_in = min([e["clock_in"] for e in employees])
        clock_out = max([e["clock_out"] for e in employees])
        hours = round((clock_out - clock_in).total_seconds() / 3600, 2)
        print(f"Hours: {hours} (IN: {clock_in.strftime('%I:%M %p')} - OUT: {clock_out.strftime('%I:%M %p')})")
        print("Team members:")
        for i, emp in enumerate(sorted(employees, key=lambda x: x["name"])):
            print(f"  {i+1}. {emp['name']} ({emp['hours']} hrs)")

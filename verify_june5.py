#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee, Squad
from datetime import datetime, timedelta
from sqlalchemy import func

with app.app_context():
    # Query for June 5, 2025 records
    june5_start = datetime(2025, 6, 5, 0, 0, 0)
    june5_end = datetime(2025, 6, 6, 0, 0, 0)
    
    records = TimeRecord.query.filter(
        TimeRecord.clock_in >= june5_start,
        TimeRecord.clock_in < june5_end
    ).all()
    
    print(f"Found {len(records)} time records for June 5, 2025")
    
    # Group by team/location
    team_locations = {}
    for record in records:
        employee = Employee.query.get(record.employee_id)
        location = record.location_in.split(',')[0] if record.location_in else "Unknown"
        
        key = location
        if key not in team_locations:
            team_locations[key] = []
        
        # Get employee's squad
        squad_name = "Unassigned"
        if employee.squad_id:
            squad = Squad.query.get(employee.squad_id)
            squad_name = squad.name if squad else "Unassigned"
        
        hours = round((record.clock_out - record.clock_in).total_seconds() / 3600, 2) if record.clock_out else 0
        
        team_locations[key].append({
            "name": employee.name,
            "squad": squad_name,
            "clock_in": record.clock_in,
            "clock_out": record.clock_out,
            "hours": hours
        })
    
    # Display team activity
    print("\nJune 5, 2025 Team Activity:")
    print("--------------------------")
    for location, employees in team_locations.items():
        print(f"\n{location} - {len(employees)} employees")
        
        # Group by squad
        squads = {}
        for emp in employees:
            if emp["squad"] not in squads:
                squads[emp["squad"]] = []
            squads[emp["squad"]].append(emp)
            
        for squad_name, squad_members in squads.items():
            if squad_members:
                clock_in = min([e["clock_in"] for e in squad_members])
                clock_out = max([e["clock_out"] for e in squad_members])
                hours = round((clock_out - clock_in).total_seconds() / 3600, 2)
                print(f"Team: {squad_name}")
                print(f"Hours: {hours} (IN: {clock_in.strftime('%I:%M %p')} - OUT: {clock_out.strftime('%I:%M %p')})")
                print("Team members:")
                for i, emp in enumerate(sorted(squad_members, key=lambda x: x["name"])):
                    print(f"  {i+1}. {emp['name']} ({emp['hours']} hrs)")

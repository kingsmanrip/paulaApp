#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime
import re

def add_june5_records():
    with app.app_context():
        # Clear any existing June 5 records to avoid duplicates
        june5_start = datetime(2025, 6, 5, 0, 0, 0)
        june5_end = datetime(2025, 6, 6, 0, 0, 0)
        existing = TimeRecord.query.filter(
            TimeRecord.clock_in >= june5_start,
            TimeRecord.clock_in < june5_end
        ).all()
        
        if existing:
            print(f"Removing {len(existing)} existing records for June 5")
            for record in existing:
                db.session.delete(record)
            db.session.commit()
        
        # Team 1: Blake Hay's team
        team1 = ["Blake Hay", "Oscar Hernandez", "Luis Velasquez", "Hector Hernandez", "Ignacio Antonio", "Jaime Garcia"]
        clock_in1 = datetime(2025, 6, 5, 7, 19)
        clock_out1 = datetime(2025, 6, 5, 15, 24)
        location_in1 = "2902 Seventh St Meridian MS 39301"
        location_out1 = "2921 40th St Meridian MS 39305"
        
        # Team 2: Joseph Mcswain's team (with Daniel Velez added to clock-in)
        team2 = ["Joseph Mcswain", "Jorge Rodas", "Carlos Guevara", "Luis Amador", "Julio Funes", "Daniel Velez"]
        clock_in2 = datetime(2025, 6, 5, 7, 33)
        clock_out2 = datetime(2025, 6, 5, 15, 12)
        location_in2 = "3510 29th Ave Meridian MS 39305"
        location_out2 = "2816 Eighth St Meridian MS 39301"
        
        # Team 3: James Jarrell's team
        team3 = ["James Jarrell", "Thomas King", "Seth Pope", "Kyzer Revette", "Richard Carter"]
        clock_in3 = datetime(2025, 6, 5, 8, 3)
        clock_out3 = datetime(2025, 6, 5, 15, 8)
        location_in3 = "5285–5299 Fairground Dr Marion MS 39342"
        location_out3 = "5201–5235 Fairground Dr Marion MS 39342"
        
        # Team 4: Cristian Pérez's team
        team4 = ["Cristian Pérez", "Yovanis Diaz", "Willy Galvez", "Eliseo Galvez", "Antonio Jimenez", "Reynaldo Martinez"]
        clock_in4 = datetime(2025, 6, 5, 7, 53)
        clock_out4 = datetime(2025, 6, 5, 15, 27)
        location_in4 = "310 Wall St W Osyka MS 39657"
        location_out4 = "1099 Second St S Osyka MS 39657"
        
        # Team 5: Caleb Bryant's team
        team5 = ["Caleb Bryant", "Seth James", "Colton Poore", "David Pool", "Shawn Beard"]
        clock_in5 = datetime(2025, 6, 5, 9, 53)
        clock_out5 = datetime(2025, 6, 5, 15, 12)
        location_in5 = "905 S Frontage Rd Meridian MS 39301"
        location_out5 = "I-20 E Meridian MS 39301"
        
        # Team 6: Johnnie Roberts' team (with Jeremy Smith and Detrick Conerly added to clock-in, middle initials removed)
        team6 = ["Jeramy Smith", "Johnnie Roberts", "Maurilio Galvez", "Rodolfo Coronado", "Jeremy Smith", "Detrick Conerly"]
        clock_in6 = datetime(2025, 6, 5, 9, 56)
        clock_out6 = datetime(2025, 6, 5, 15, 58)
        location_in6 = "1106 Second St N Osyka MS 39667"
        location_out6 = "US-98 E Tylertown MS 39667"
        
        teams = [team1, team2, team3, team4, team5, team6]
        clock_ins = [clock_in1, clock_in2, clock_in3, clock_in4, clock_in5, clock_in6]
        clock_outs = [clock_out1, clock_out2, clock_out3, clock_out4, clock_out5, clock_out6]
        location_ins = [location_in1, location_in2, location_in3, location_in4, location_in5, location_in6]
        location_outs = [location_out1, location_out2, location_out3, location_out4, location_out5, location_out6]
        
        # Process each team
        records_added = 0
        for i, team in enumerate(teams):
            for name in team:
                # Find the employee - handle names with middle initials by stripping them
                # First try exact match
                employee = Employee.query.filter(Employee.name.ilike(f"%{name}%")).first()
                
                if not employee:
                    print(f"⚠️ Employee not found: {name}")
                    # If this is a new employee, we'd need to create them
                    continue
                
                # Create time record
                record = TimeRecord(
                    employee_id=employee.id,
                    clock_in=clock_ins[i],
                    clock_out=clock_outs[i],
                    location_in=location_ins[i],
                    location_out=location_outs[i]
                )
                db.session.add(record)
                records_added += 1
                print(f"Added time record for {name}")
            
        # Commit all changes
        db.session.commit()
        print(f"\nAll {records_added} June 5, 2025 time records have been imported!")

if __name__ == "__main__":
    add_june5_records()

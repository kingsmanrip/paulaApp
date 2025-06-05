#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime
import re

def add_june4_records():
    with app.app_context():
        # Clear any existing June 4 records to avoid duplicates
        june4_start = datetime(2025, 6, 4, 0, 0, 0)
        june4_end = datetime(2025, 6, 5, 0, 0, 0)
        existing = TimeRecord.query.filter(
            TimeRecord.clock_in >= june4_start,
            TimeRecord.clock_in < june4_end
        ).all()
        
        if existing:
            print(f"Removing {len(existing)} existing records for June 4")
            for record in existing:
                db.session.delete(record)
            db.session.commit()
        
        # Team 1: Joseph Mcswain's team
        team1 = ["Joseph Mcswain", "Jorge Rodas", "Daniel Velez", "Carlos Guevara", "Luis Amador", "Julio Funes"]
        clock_in1 = datetime(2025, 6, 4, 7, 19)
        clock_out1 = datetime(2025, 6, 4, 16, 7)
        location_in1 = "2820 Valley St Meridian MS 39301"
        location_out1 = "4005 Poplar Springs Dr Meridian MS 39305"
        
        # Team 2: Blake Hay's team (now with Jaime Garcia)
        team2 = ["Blake Hay", "Oscar Hernandez", "Luis Velasquez", "Hector Hernandez", "Ignacio Antonio", "Jaime Garcia"]
        clock_in2 = datetime(2025, 6, 4, 7, 37)
        clock_out2 = datetime(2025, 6, 4, 15, 14)
        location_in2 = "2837 29th Ave Meridian MS 39305"
        location_out2 = "2522 40th St Meridian MS 39305"
        
        # Team 3: Cristian Pérez's team (now with Eliseo Galvez)
        team3 = ["Cristian Pérez", "Yovanis Diaz", "Willy Galvez", "Eliseo Galvez", "Antonio Jimenez", "Reynaldo Martinez"]
        clock_in3 = datetime(2025, 6, 4, 8, 0)
        clock_out3 = datetime(2025, 6, 4, 16, 15)
        location_in3 = "1091 Second St S Osyka MS 39657"
        location_out3 = "102 E Liberty St Osyka MS 39657"
        
        # Team 4: Caleb Bryant's team (back with his regular team)
        team4 = ["Caleb Bryant", "Aaron Mitchell", "Seth James", "Colton Poore", "David Pool"]
        clock_in4 = datetime(2025, 6, 4, 8, 19)
        clock_out4 = datetime(2025, 6, 4, 16, 33)
        location_in4 = "618 Ninth Ave NW Magee MS 39111"
        location_out4 = "602 11th Ave NW Magee MS 39111"
        
        # Team 5: Johnnie Roberts' team (original team configuration)
        team5 = ["Jeramy Smith", "Johnnie Roberts", "Maurilio Galvez", "Rodolfo Coronado"]
        clock_in5 = datetime(2025, 6, 4, 8, 32)
        clock_out5 = datetime(2025, 6, 4, 17, 23)
        location_in5 = "1106 Second St N Osyka MS 39667"
        location_out5 = "US-98 W Sumrall MS 39482"
        
        # Team 6: James Jarrell's team
        team6 = ["James Jarrell", "Thomas King", "Seth Pope", "Kyzer Revette", "Richard Carter"]
        clock_in6 = datetime(2025, 6, 4, 8, 37)
        clock_out6 = datetime(2025, 6, 4, 14, 35)
        location_in6 = "4858 Marion Dr Marion MS 39342"
        location_out6 = "2671–2675 N Frontage Rd Meridian MS 39301"
        
        teams = [team1, team2, team3, team4, team5, team6]
        clock_ins = [clock_in1, clock_in2, clock_in3, clock_in4, clock_in5, clock_in6]
        clock_outs = [clock_out1, clock_out2, clock_out3, clock_out4, clock_out5, clock_out6]
        location_ins = [location_in1, location_in2, location_in3, location_in4, location_in5, location_in6]
        location_outs = [location_out1, location_out2, location_out3, location_out4, location_out5, location_out6]
        
        # Process each team
        records_added = 0
        for i, team in enumerate(teams):
            for name in team:
                # Find the employee
                employee = Employee.query.filter(Employee.name.ilike(f"%{name}%")).first()
                if not employee:
                    print(f"⚠️ Employee not found: {name}")
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
        print(f"\nAll {records_added} June 4, 2025 time records have been imported!")

if __name__ == "__main__":
    add_june4_records()

#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime
import re

def add_june3_records():
    with app.app_context():
        # Clear any existing June 3 records to avoid duplicates
        june3_start = datetime(2025, 6, 3, 0, 0, 0)
        june3_end = datetime(2025, 6, 4, 0, 0, 0)
        existing = TimeRecord.query.filter(
            TimeRecord.clock_in >= june3_start,
            TimeRecord.clock_in < june3_end
        ).all()
        
        if existing:
            print(f"Removing {len(existing)} existing records for June 3")
            for record in existing:
                db.session.delete(record)
            db.session.commit()
        
        # Team 1: Joseph Mcswain's team
        team1 = ["Joseph Mcswain", "Jorge Rodas", "Daniel Velez", "Carlos Guevara", "Luis Amador", "Julio Funes"]
        clock_in1 = datetime(2025, 6, 3, 7, 18)
        clock_out1 = datetime(2025, 6, 3, 16, 4)
        location_in1 = "1619 29th Ave Meridian MS 39301"
        location_out1 = "1820 29th Ave Meridian MS 39301"
        
        # Team 2: Taiwan Brown's team (without him, but with his members)
        team2 = ["Blake Hay", "Oscar Hernandez", "Luis Velasquez", "Hector Hernandez", "Ignacio Antonio"]
        clock_in2 = datetime(2025, 6, 3, 7, 30)
        clock_out2 = datetime(2025, 6, 3, 16, 18)
        location_in2 = "3930 Poplar Springs Dr Meridian MS 39305"
        location_out2 = "I-59 S Enterprise MS 39330"
        
        # Team 3: James Jarrell's team (with Seth Pope back)
        team3 = ["James Jarrell", "Thomas King", "Seth Pope", "Kyzer Revette", "Richard Carter"]
        clock_in3 = datetime(2025, 6, 3, 7, 49)
        clock_out3 = datetime(2025, 6, 3, 15, 40)
        location_in3 = "4768 Marion Dr Marion MS 39342"
        location_out3 = "4530 Dale Dr Marion MS 39342"
        
        # Team 4: Cristian Pérez's team
        team4 = ["Cristian Pérez", "Yovanis Diaz", "Willy Galvez", "Antonio Jimenez", "Reynaldo Martinez"]
        clock_in4 = datetime(2025, 6, 3, 8, 15)
        clock_out4 = datetime(2025, 6, 3, 15, 54)
        location_in4 = "683 Fourth St N Osyka MS 39657"
        location_out4 = "310 Wall St W Osyka MS 39657"
        
        # Team 5: Combined Team (Caleb's team members + Johnnie's team)
        team5 = ["Aaron Mitchell", "Seth James", "Colton Poore", "David Pool", "Shawn Beard", 
                "Jeramy Smith", "Johnnie Roberts", "Maurilio Galvez", "Rodolfo Coronado"]
        clock_in5 = datetime(2025, 6, 3, 9, 19)
        clock_out5 = datetime(2025, 6, 3, 17, 10)
        location_in5 = "607 Cherry St NW Magee MS 39111"
        location_out5 = "603 Cherry St NW Magee MS 39111"
        
        teams = [team1, team2, team3, team4, team5]
        clock_ins = [clock_in1, clock_in2, clock_in3, clock_in4, clock_in5]
        clock_outs = [clock_out1, clock_out2, clock_out3, clock_out4, clock_out5]
        location_ins = [location_in1, location_in2, location_in3, location_in4, location_in5]
        location_outs = [location_out1, location_out2, location_out3, location_out4, location_out5]
        
        # Process each team
        for i, team in enumerate(teams):
            for name in team:
                # Find the employee
                employee = Employee.query.filter(Employee.name.ilike(f"%{name}%")).first()
                if not employee:
                    print(f"Employee not found: {name}")
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
                print(f"Added time record for {name}")
            
        # Commit all changes
        db.session.commit()
        print("All June 3, 2025 time records have been imported!")

if __name__ == "__main__":
    add_june3_records()

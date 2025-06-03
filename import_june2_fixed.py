#!/usr/bin/env python3
from app import app, db, TimeRecord, Employee
from datetime import datetime
import re

def format_date(date_str):
    # Normalize the date format to handle different variants
    date_str = date_str.lower().strip()
    
    # Replace "at" with a comma
    date_str = date_str.replace(' at ', ', ')
    
    # Handle a.m./p.m. format
    date_str = date_str.replace('a.m.', 'am').replace('p.m.', 'pm')
    
    # Remove Estados Unidos or United States
    date_str = date_str.replace('estados unidos', '').replace('united states', '').strip()
    
    # Try to parse with different formats
    formats = [
        '%b %d, %Y, %I:%M %p',
        '%b %d, %Y, %I:%M%p',
        '%B %d, %Y, %I:%M %p',
        '%B %d, %Y, %I:%M%p'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # If we get here, none of the formats worked
    print(f"Could not parse date: {date_str}")
    # Use a fixed date as fallback
    return datetime(2025, 6, 2, 12, 0, 0)

def add_time_records():
    with app.app_context():
        # Clear any existing June 2 records to avoid duplicates
        june2_start = datetime(2025, 6, 2, 0, 0, 0)
        june2_end = datetime(2025, 6, 3, 0, 0, 0)
        existing = TimeRecord.query.filter(
            TimeRecord.clock_in >= june2_start,
            TimeRecord.clock_in < june2_end
        ).all()
        
        if existing:
            print(f"Removing {len(existing)} existing records for June 2")
            for record in existing:
                db.session.delete(record)
            db.session.commit()
        
        # Team 1: Joseph Mcswain's team
        team1 = ["Joseph Mcswain", "Jorge Rodas", "Daniel Velez", "Carlos Guevara", "Luis Amador", "Julio Funes"]
        clock_in1 = datetime(2025, 6, 2, 7, 27)
        clock_out1 = datetime(2025, 6, 2, 15, 58)
        location_in1 = "3330 28th Ave Meridian MS 39305"
        location_out1 = "29th Ave Meridian MS 39301"
        
        # Team 2: Mixed team with Blake Hay
        team2 = ["Blake Hay", "Oscar Hernandez", "Luis Velasquez", "Hector Hernandez", "Ignacio Antonio", "Jaime Garcia"]
        clock_in2 = datetime(2025, 6, 2, 7, 40)
        clock_out2 = datetime(2025, 6, 2, 15, 30)
        location_in2 = "3930 Poplar Springs Dr Meridian MS 39305"
        location_out2 = "2725 40th St Meridian MS 39305"
        
        # Team 3: James Jarrell's team
        team3 = ["James Jarrell", "Thomas King", "Kyzer Revette", "Richard Carter"]
        clock_in3 = datetime(2025, 6, 2, 7, 42)
        clock_out3 = datetime(2025, 6, 2, 16, 39)
        location_in3 = "5401 Marion Dr Marion MS 39342"
        location_out3 = "820–844 NE Industrial Park Rd Marion MS 39342"
        
        # Team 4: Cristian Pérez's team
        team4 = ["Cristian Pérez", "Yovanis Diaz", "Willy Galvez", "Antonio Jimenez", "Reynaldo Martinez"]
        clock_in4 = datetime(2025, 6, 2, 8, 1)
        clock_out4 = datetime(2025, 6, 2, 15, 55)
        location_in4 = "333 W Amite St Osyka MS 39657"
        location_out4 = "E Liberty St Osyka MS 39657"
        
        # Team 5: Caleb Bryant's team
        team5 = ["Caleb Bryant", "Aaron Mitchell", "Seth James", "Colton Poore", "David Pool", "Shawn Beard"]
        clock_in5 = datetime(2025, 6, 2, 8, 21)
        clock_out5 = datetime(2025, 6, 2, 16, 28)
        location_in5 = "479 Simpson Hwy 149 Magee MS 39111"
        location_out5 = "642 Ninth Ave NW Magee MS 39111"
        
        # Team 6: Johnnie Roberts' team
        team6 = ["Jeramy Smith", "Johnnie Roberts", "Maurilio Galvez", "Rodolfo Coronado"]
        clock_in6 = datetime(2025, 6, 2, 8, 50)
        clock_out6 = datetime(2025, 6, 2, 16, 3)
        location_in6 = "529 Elm Ave NW Magee MS 39111"
        location_out6 = "521 Elm Ave NW Magee MS 39111"
        
        teams = [team1, team2, team3, team4, team5, team6]
        clock_ins = [clock_in1, clock_in2, clock_in3, clock_in4, clock_in5, clock_in6]
        clock_outs = [clock_out1, clock_out2, clock_out3, clock_out4, clock_out5, clock_out6]
        location_ins = [location_in1, location_in2, location_in3, location_in4, location_in5, location_in6]
        location_outs = [location_out1, location_out2, location_out3, location_out4, location_out5, location_out6]
        
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
        print("All June 2, 2025 time records have been imported!")

if __name__ == "__main__":
    add_time_records()

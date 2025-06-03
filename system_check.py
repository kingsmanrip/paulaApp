#!/usr/bin/env python3
from app import app, db, Employee, Squad, TimeRecord, User
from datetime import datetime, timedelta
import sys

def check_database():
    """Check database tables and counts"""
    print("\n===== DATABASE INTEGRITY CHECK =====")
    print(f"Employees: {Employee.query.count()}")
    print(f"Squads: {Squad.query.count()}")
    print(f"Time Records: {TimeRecord.query.count()}")
    print(f"Users: {User.query.count()}")
    
    # Check for orphaned records
    orphaned = TimeRecord.query.filter(~TimeRecord.employee_id.in_(
        db.session.query(Employee.id)
    )).count()
    print(f"Orphaned time records: {orphaned}")
    
    # Check squad assignments
    unassigned = Employee.query.filter_by(squad_id=None).count()
    print(f"Unassigned employees: {unassigned}")
    
    # Check squad leaders
    squads_with_leaders = Squad.query.filter(Squad.squad_leader_id.isnot(None)).count()
    print(f"Squads with leaders: {squads_with_leaders} out of {Squad.query.count()}")

def check_recent_records():
    """Check recent time records"""
    print("\n===== RECENT TIME RECORDS CHECK =====")
    now = datetime.now()
    
    # Check June 2 records
    june2_start = datetime(2025, 6, 2, 0, 0, 0)
    june2_end = datetime(2025, 6, 3, 0, 0, 0)
    june2_records = TimeRecord.query.filter(
        TimeRecord.clock_in >= june2_start,
        TimeRecord.clock_in < june2_end
    ).count()
    print(f"June 2, 2025 records: {june2_records}")
    
    # Check for incomplete records (missing clock-out)
    incomplete = TimeRecord.query.filter(
        TimeRecord.clock_in.isnot(None),
        TimeRecord.clock_out.is_(None)
    ).count()
    print(f"Incomplete records (missing clock-out): {incomplete}")
    
    # Check for standalone clock-outs (missing clock-in)
    standalone_outs = TimeRecord.query.filter(
        TimeRecord.clock_in.is_(None),
        TimeRecord.clock_out.isnot(None)
    ).count()
    print(f"Standalone clock-outs (missing clock-in): {standalone_outs}")
    
    # Sample of recent records
    print("\nSample of 5 recent time records:")
    recent = TimeRecord.query.order_by(TimeRecord.clock_in.desc()).limit(5).all()
    for r in recent:
        emp = Employee.query.get(r.employee_id)
        print(f"- {emp.name}: IN: {r.clock_in} at {r.location_in[:20]}... OUT: {r.clock_out} at {r.location_out[:20] if r.location_out else 'N/A'}")

def check_hours_calculations():
    """Check hours calculations for accuracy"""
    print("\n===== HOURS CALCULATION CHECK =====")
    # Sample employee
    emp = Employee.query.first()
    if not emp:
        print("No employees found to check hours calculations")
        return
        
    # Sample time record for testing
    test_record = TimeRecord(
        employee_id=emp.id,
        clock_in=datetime(2025, 6, 2, 8, 0, 0),
        clock_out=datetime(2025, 6, 2, 17, 0, 0),
        location_in="Test location in",
        location_out="Test location out"
    )
    
    # Calculate hours manually
    hours = (test_record.clock_out - test_record.clock_in).total_seconds() / 3600
    print(f"Test record duration: {hours} hours")
    
    # Query hours using SQL
    from sqlalchemy import func
    sql_hours = db.session.query(
        func.julianday(test_record.clock_out) - func.julianday(test_record.clock_in)
    ).scalar() * 24
    
    print(f"SQL calculation: {sql_hours} hours")
    print(f"Calculation match: {'Yes' if abs(hours - sql_hours) < 0.01 else 'No'}")

def check_routes():
    """Check critical application routes"""
    print("\n===== ROUTE CHECK =====")
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append((rule.endpoint, rule.methods, rule.rule))
    
    # Check for essential routes
    essential_routes = ['login', 'dashboard', 'logout', 'employee_detail', 'bulk_import', 'analytics']
    for route in essential_routes:
        found = any(r[0] == route for r in routes)
        print(f"Route '{route}': {'✓' if found else '✗'}")
    
    # Check for week navigation in dashboard route
    dashboard_routes = [r for r in routes if r[0] == 'dashboard']
    has_week_nav = any('<string:week_date>' in r[2] for r in dashboard_routes)
    print(f"Week navigation support: {'✓' if has_week_nav else '✗'}")

def main():
    with app.app_context():
        try:
            check_database()
            check_recent_records()
            check_hours_calculations()
            check_routes()
            print("\n✅ System check completed successfully!")
        except Exception as e:
            print(f"\n❌ System check failed: {str(e)}")
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

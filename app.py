from flask import Flask, render_template, redirect, url_for, request, flash, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_weasyprint import HTML, render_pdf
import os
import io
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'employee-tracker-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Squad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    squad_leader_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    employees = db.relationship('Employee', backref='squad', foreign_keys='Employee.squad_id', lazy=True)
    squad_leader = db.relationship('Employee', foreign_keys=[squad_leader_id], backref='leading_squad', uselist=False, lazy=True, post_update=True)
    
    def __repr__(self):
        return f'<Squad {self.name}>'

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    squad_id = db.Column(db.Integer, db.ForeignKey('squad.id'), nullable=True)
    timerecords = db.relationship('TimeRecord', backref='employee', lazy=True)
    
    def __repr__(self):
        return f'<Employee {self.name}>'

class TimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    clock_in = db.Column(db.DateTime, nullable=False)
    clock_out = db.Column(db.DateTime, nullable=True)
    location_in = db.Column(db.String(200), nullable=False)
    location_out = db.Column(db.String(200), nullable=True)
    
    def hours_worked(self):
        if self.clock_out:
            delta = self.clock_out - self.clock_in
            return round(delta.total_seconds() / 3600, 2)
        return 0
    
    def __repr__(self):
        return f'<TimeRecord {self.employee.name} {self.clock_in.strftime("%Y-%m-%d")}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    employees = Employee.query.all()
    squads = Squad.query.all()
    today = datetime.now().date()
    
    # Get date range for current week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get the latest day with time records
    latest_workday = get_latest_workday()
    
    # Generate insights
    insights = []
    
    # Find top performing squad
    squad_hours = {}
    for squad in squads:
        total_hours = sum(calculate_total_hours(employee) for employee in squad.employees)
        squad_hours[squad.id] = total_hours
    
    if squad_hours:
        top_squad_id = max(squad_hours, key=squad_hours.get) if squad_hours else None
        if top_squad_id:
            top_squad = Squad.query.get(top_squad_id)
            insights.append(f"Top performing squad: {top_squad.name} with {squad_hours[top_squad_id]:.1f} hours")
    
    # Find employees with no recent activity (7 days)
    inactive_employees = []
    week_ago = today - timedelta(days=7)
    
    for employee in employees:
        recent_record = TimeRecord.query.filter(
            TimeRecord.employee_id == employee.id,
            TimeRecord.clock_in >= datetime.combine(week_ago, datetime.min.time())
        ).first()
        
        if not recent_record:
            inactive_employees.append(employee.name)
    
    if inactive_employees:
        insights.append(f"Employees with no activity in the last week: {', '.join(inactive_employees)}")
    
    # Find underperforming employees (avg < 8 hours per day)
    underperforming = []
    for employee in employees:
        records = TimeRecord.query.filter(
            TimeRecord.employee_id == employee.id,
            TimeRecord.clock_in >= datetime.combine(week_ago, datetime.min.time())
        ).all()
        
        if records:
            total_hours = sum(record.hours_worked() for record in records if record.clock_out)
            unique_days = len(set(record.clock_in.date() for record in records))
            avg_hours = total_hours / unique_days if unique_days > 0 else 0
            
            if avg_hours < 8 and avg_hours > 0:
                underperforming.append(f"{employee.name} ({avg_hours:.1f} hrs/day)")
    
    if underperforming:
        insights.append(f"Underperforming employees (< 8hrs/day): {', '.join(underperforming[:3])}" + 
                       (" and others" if len(underperforming) > 3 else ""))
    
    # Detect unusual patterns
    unusual_patterns = []
    for employee in employees:
        records = TimeRecord.query.filter(
            TimeRecord.employee_id == employee.id,
            TimeRecord.clock_in >= datetime.combine(week_ago, datetime.min.time())
        ).all()
        
        for record in records:
            if record.clock_out and record.hours_worked() > 12:
                unusual_patterns.append(f"{employee.name} worked {record.hours_worked():.1f} hours on {record.clock_in.strftime('%Y-%m-%d')}")
    
    if unusual_patterns:
        insights.append(f"Unusual work patterns detected: {unusual_patterns[0]}" + 
                       (" and others" if len(unusual_patterns) > 1 else ""))
    
    return render_template('dashboard.html', 
                          employees=employees, 
                          calculate_total_hours=calculate_total_hours,
                          today=today, 
                          squads=squads,
                          insights=insights,
                          latest_workday=latest_workday,
                          start_of_week=start_of_week,
                          end_of_week=end_of_week)

@app.route('/employee/<int:employee_id>')
@login_required
def employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    # Get date range for current week (Monday to Sunday)
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get records for current week
    week_records = TimeRecord.query.filter(
        TimeRecord.employee_id == employee_id,
        TimeRecord.clock_in >= datetime.combine(start_of_week, datetime.min.time()),
        TimeRecord.clock_in <= datetime.combine(end_of_week, datetime.max.time())
    ).all()
    
    # Get all records for the employee
    all_records = TimeRecord.query.filter_by(employee_id=employee_id).order_by(TimeRecord.clock_in.desc()).all()
    
    return render_template('employee_detail.html', 
                          employee=employee,
                          week_records=week_records,
                          all_records=all_records,
                          start_of_week=start_of_week,
                          end_of_week=end_of_week)

@app.route('/add_record', methods=['GET', 'POST'])
@login_required
def add_record():
    employees = Employee.query.all()
    
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        clock_in_date = request.form.get('clock_in_date')
        clock_in_time = request.form.get('clock_in_time')
        clock_out_date = request.form.get('clock_out_date')
        clock_out_time = request.form.get('clock_out_time')
        location_in = request.form.get('location_in')
        location_out = request.form.get('location_out')
        
        # Combine date and time into datetime objects
        clock_in = datetime.strptime(f"{clock_in_date} {clock_in_time}", "%Y-%m-%d %H:%M")
        
        if clock_out_date and clock_out_time:
            clock_out = datetime.strptime(f"{clock_out_date} {clock_out_time}", "%Y-%m-%d %H:%M")
        else:
            clock_out = None
            
        record = TimeRecord(
            employee_id=employee_id,
            clock_in=clock_in,
            clock_out=clock_out,
            location_in=location_in,
            location_out=location_out if location_out else None
        )
        
        db.session.add(record)
        db.session.commit()
        
        flash('Record added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_record.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash('Employee name is required!')
            return redirect(url_for('add_employee'))
        
        employee = Employee(name=name)
        db.session.add(employee)
        db.session.commit()
        
        flash('Employee added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_employee.html')

@app.route('/bulk_import', methods=['GET', 'POST'])
@login_required
def bulk_import():
    if request.method == 'POST':
        data = request.form.get('data')
        
        # Parse the multi-line format
        current_action = None
        employee_names = ""
        location = ""
        date_str = ""
        
        lines = data.strip().split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Determine record type (ClockIn/ClockOut)
            if line.startswith("ClockIn-"):
                current_action = "ClockIn"
                i += 1
                
                # Find employee section
                while i < len(lines) and not lines[i].strip().startswith("employee:"):
                    i += 1
                
                if i < len(lines):  # Found employee section
                    i += 1  # Move past the "employee:" line
                    employee_names = ""
                    
                    # Collect all employee names until we hit "location:"
                    while i < len(lines) and not lines[i].strip().startswith("location:"):
                        employee_names += lines[i].strip() + " "
                        i += 1
                    
                    if i < len(lines):  # Found location section
                        i += 1  # Move past the "location:" line
                        location = ""
                        
                        # Collect location until we hit "date:"
                        while i < len(lines) and not lines[i].strip().startswith("date:"):
                            location += lines[i].strip() + "\n"
                            i += 1
                        
                        location = location.strip()
                        
                        if i < len(lines):  # Found date section
                            i += 1  # Move past the "date:" line
                            date_str = lines[i].strip()
                            
                            # Process the clock-in record with collected data
                            try:
                                date_obj = datetime.strptime(date_str, '%B %d, %Y at %I:%M %p')
                                
                                # Process each employee
                                for emp_name in employee_names.split():
                                    if not emp_name or emp_name in ["and"]:
                                        continue
                                    
                                    # Try to find employee
                                    employee = Employee.query.filter_by(name=emp_name).first()
                                    if not employee:
                                        continue
                                    
                                    # Check if there's already a clock-in record for this employee on this date
                                    existing_record = TimeRecord.query.filter(
                                        TimeRecord.employee_id == employee.id,
                                        TimeRecord.clock_in.date() == date_obj.date()
                                    ).first()
                                    
                                    if existing_record:
                                        existing_record.clock_in = date_obj
                                        existing_record.location_in = location
                                    else:
                                        record = TimeRecord(
                                            employee_id=employee.id,
                                            clock_in=date_obj,
                                            location_in=location
                                        )
                                        db.session.add(record)
                                    
                                    db.session.commit()
                                    
                            except ValueError as e:
                                flash(f'Error processing record: {str(e)}')
                
            elif line.startswith("ClockOut-"):
                current_action = "ClockOut"
                i += 1
                
                # Find employee section
                while i < len(lines) and not lines[i].strip().startswith("employee:"):
                    i += 1
                
                if i < len(lines):  # Found employee section
                    i += 1  # Move past the "employee:" line
                    employee_names = ""
                    
                    # Collect all employee names until we hit "location:"
                    while i < len(lines) and not lines[i].strip().startswith("location:"):
                        employee_names += lines[i].strip() + " "
                        i += 1
                    
                    if i < len(lines):  # Found location section
                        i += 1  # Move past the "location:" line
                        location = ""
                        
                        # Collect location until we hit "date:"
                        while i < len(lines) and not lines[i].strip().startswith("date:"):
                            location += lines[i].strip() + "\n"
                            i += 1
                        
                        location = location.strip()
                        
                        if i < len(lines):  # Found date section
                            i += 1  # Move past the "date:" line
                            date_str = lines[i].strip()
                            
                            # Process the clock-out record with collected data
                            try:
                                date_obj = datetime.strptime(date_str, '%B %d, %Y at %I:%M %p')
                                
                                # Process each employee
                                for emp_name in employee_names.split():
                                    if not emp_name or emp_name in ["and"]:
                                        continue
                                    
                                    # Try to find employee
                                    employee = Employee.query.filter_by(name=emp_name).first()
                                    if not employee:
                                        continue
                                    
                                    # Find the most recent clock-in record without a clock-out
                                    record = TimeRecord.query.filter(
                                        TimeRecord.employee_id == employee.id,
                                        TimeRecord.clock_in.date() == date_obj.date(),
                                        TimeRecord.clock_out == None
                                    ).first()
                                    
                                    if record:
                                        record.clock_out = date_obj
                                        record.location_out = location
                                        db.session.commit()
                                    
                            except ValueError as e:
                                flash(f'Error processing record: {str(e)}')
            else:
                i += 1
        
        flash('Data imported successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('bulk_import.html')

def calculate_total_hours(employee, start_date=None, end_date=None):
    """Calculate total hours worked by an employee within a date range"""
    # Import text function from SQLAlchemy
    from sqlalchemy import text
    
    # Base query
    sql_query = """
    SELECT ROUND(SUM((julianday(clock_out) - julianday(clock_in)) * 24), 2) as total_hours
    FROM time_record 
    WHERE employee_id = :employee_id AND clock_out IS NOT NULL
    """
    
    # Parameters dictionary
    params = {"employee_id": employee.id}
    
    if start_date:
        sql_query += " AND date(clock_in) >= date(:start_date)"
        params["start_date"] = start_date.strftime('%Y-%m-%d')
        
    if end_date:
        sql_query += " AND date(clock_in) <= date(:end_date)"
        params["end_date"] = end_date.strftime('%Y-%m-%d')
    
    # Execute with proper text() function
    result = db.session.execute(text(sql_query), params).fetchone()
    
    # Handle None result (no hours worked)
    if result and result[0] is not None:
        return result[0]
    return 0.0

def get_latest_workday(employee=None):
    """Get the most recent day that has time records"""
    query = TimeRecord.query
    if employee:
        query = query.filter_by(employee_id=employee.id)
    
    # Find the latest record that has a clock_out time (completed record)
    latest_record = query.filter(TimeRecord.clock_out.isnot(None)).order_by(TimeRecord.clock_in.desc()).first()
    if latest_record:
        return latest_record.clock_in.date()
    return datetime.today().date()

@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %I:%M %p'):
    if value:
        return value.strftime(format)
    return ""

@app.route('/reports')
@login_required
def reports():
    squads = Squad.query.all()
    employees = Employee.query.all()
    return render_template('reports.html', squads=squads, employees=employees)

@app.route('/generate_pdf', methods=['POST'])
@login_required
def generate_pdf():
    # Get form data
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    report_type = request.form.get('report_type')
    report_format = request.form.get('report_format')
    squad_id = request.form.get('squad_id')
    employee_id = request.form.get('employee_id')
    report_title = request.form.get('report_title')
    
    # Parse dates
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Use default title if none provided
    if not report_title:
        if report_type == 'all':
            report_title = 'All Employees Hours Report'
        elif report_type == 'squad':
            squad = Squad.query.get(squad_id)
            report_title = f'{squad.name} Squad Hours Report' if squad else 'Squad Hours Report'
        else:
            employee = Employee.query.get(employee_id)
            report_title = f'{employee.name} Hours Report' if employee else 'Employee Hours Report'
    
    # Get data based on report type
    squads = []
    single_employee = None
    
    if report_type == 'all':
        squads = Squad.query.all()
    elif report_type == 'squad' and squad_id:
        squad = Squad.query.get(squad_id)
        if squad:
            squads = [squad]
    elif report_type == 'employee' and employee_id:
        single_employee = Employee.query.get(employee_id)
    
    # Get all relevant employees
    employees = []
    if report_type == 'all' or report_type == 'squad':
        for squad in squads:
            employees.extend(squad.employees)
    elif single_employee:
        employees = [single_employee]
    
    # Prepare data structures for report
    employee_records = {}
    employee_totals = {}
    squad_totals = defaultdict(float)
    total_hours = 0
    
    # Get time records for each employee in the date range
    for employee in employees:
        # Filter records by date range
        records = TimeRecord.query.filter(
            TimeRecord.employee_id == employee.id,
            TimeRecord.clock_in >= datetime.combine(start_date, datetime.min.time()),
            TimeRecord.clock_in <= datetime.combine(end_date, datetime.max.time())
        ).order_by(TimeRecord.clock_in).all()
        
        # Store records for this employee
        employee_records[employee.id] = records
        
        # Calculate totals for this employee
        hours = sum(record.hours_worked() for record in records)
        unique_days = len(set(record.clock_in.date() for record in records))
        
        employee_totals[employee.id] = {
            'hours': round(hours, 2),
            'days': unique_days
        }
        
        # Add to squad total if applicable
        if employee.squad_id:
            squad_totals[employee.squad_id] += hours
        
        # Add to overall total
        total_hours += hours
    
    # Round squad totals
    for squad_id in squad_totals:
        squad_totals[squad_id] = round(squad_totals[squad_id], 2)
    
    # Get squad name if single squad
    squad_name = None
    if report_type == 'squad' and squads:
        squad_name = squads[0].name
    elif single_employee and single_employee.squad:
        squad_name = single_employee.squad.name
    
    # Render PDF template
    html = render_template(
        'pdf_report.html',
        title=report_title,
        start_date=start_date,
        end_date=end_date,
        report_type=report_type,
        report_format=report_format,
        squads=squads,
        single_employee=single_employee,
        employee_records=employee_records,
        employee_totals=employee_totals,
        squad_totals=squad_totals,
        total_hours=round(total_hours, 2),
        employees_count=len(employees),
        squad_name=squad_name,
        now=datetime.now()
    )
    
    # Generate PDF
    return render_pdf(HTML(string=html))

@app.route('/analytics')
@login_required
def analytics():
    # Get all employees and squads
    employees = Employee.query.all()
    squads = Squad.query.all()
    
    # Calculate data for charts
    daily_hours = defaultdict(float)
    squad_hours = defaultdict(float)
    location_data = defaultdict(int)
    employee_avg_hours = {}
    employee_last_active = {}
    
    # Get date ranges
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Track total hours and active days
    total_hours_all_time = 0
    active_days = set()
    
    # Process all time records
    time_records = TimeRecord.query.all()
    for record in time_records:
        if record.clock_out:
            hours = record.hours_worked()
            total_hours_all_time += hours
            
            # Only include last 30 days in daily chart
            if record.clock_in.date() >= thirty_days_ago:
                day = record.clock_in.strftime('%Y-%m-%d')
                daily_hours[day] += hours
                active_days.add(day)
            
            employee = Employee.query.get(record.employee_id)
            
            # Update last active date for employee
            if employee.id not in employee_last_active or record.clock_in > datetime.strptime(employee_last_active[employee.id], '%Y-%m-%d'):
                employee_last_active[employee.id] = record.clock_in.strftime('%Y-%m-%d')
            
            if employee and employee.squad_id:
                squad_hours[employee.squad_id] += hours
            
            if record.location_in:
                location = record.location_in.split('\n')[0] if '\n' in record.location_in else record.location_in
                location_data[location] += 1
    
    # Calculate average daily hours
    avg_daily_hours = round(total_hours_all_time / len(active_days), 2) if active_days else 0
    
    # Calculate employee average hours per day
    for employee in employees:
        records = TimeRecord.query.filter_by(employee_id=employee.id).all()
        if records:
            total_hours = sum(record.hours_worked() for record in records if record.clock_out)
            unique_days = len(set(record.clock_in.date() for record in records))
            avg_hours = round(total_hours / unique_days, 2) if unique_days > 0 else 0
            employee_avg_hours[employee.id] = avg_hours
        else:
            employee_avg_hours[employee.id] = 0
            employee_last_active[employee.id] = 'Never'
    
    # Sort squad hours to find top squad
    top_squad = None
    if squad_hours:
        top_squad_id = max(squad_hours, key=squad_hours.get)
        top_squad = Squad.query.get(top_squad_id)
    
    # Sort employees by average hours
    sorted_employees = sorted(employees, key=lambda e: employee_avg_hours.get(e.id, 0), reverse=True)
    top_employees = sorted_employees[:10]  # Top 10 employees
    
    # Find underperforming employees (< 8 hours/day)
    underperforming_employees = [e for e in employees if employee_avg_hours.get(e.id, 0) > 0 and employee_avg_hours.get(e.id, 0) < 8]
    underperforming_count = len(underperforming_employees)
    
    # Sort daily hours chronologically
    daily_hours = dict(sorted(daily_hours.items()))
    
    # Get top 5 locations
    top_locations = dict(sorted(location_data.items(), key=lambda x: x[1], reverse=True)[:5])
    
    # Generate insights for analytics page
    insights = []
    
    # Add top squad insight
    if top_squad:
        insights.append(f"Top performing squad: {top_squad.name} with {squad_hours[top_squad_id]:.1f} hours")
    
    # Find employees with no recent activity (7 days)
    inactive_employees = []
    week_ago = today - timedelta(days=7)
    
    for employee in employees:
        recent_record = TimeRecord.query.filter(
            TimeRecord.employee_id == employee.id,
            TimeRecord.clock_in >= datetime.combine(week_ago, datetime.min.time())
        ).first()
        
        if not recent_record:
            inactive_employees.append(employee.name)
    
    if inactive_employees:
        insights.append(f"Employees with no activity in the last week: {', '.join(inactive_employees)}")
    
    # Add underperforming employees insight
    underperforming_names = [f"{e.name} ({employee_avg_hours[e.id]:.1f} hrs/day)" for e in underperforming_employees[:3]]
    if underperforming_names:
        insights.append(f"Underperforming employees (< 8hrs/day): {', '.join(underperforming_names)}" + 
                      (" and others" if len(underperforming_employees) > 3 else ""))
    
    # Detect unusual patterns
    unusual_patterns = []
    for employee in employees:
        records = TimeRecord.query.filter(
            TimeRecord.employee_id == employee.id,
            TimeRecord.clock_in >= datetime.combine(week_ago, datetime.min.time())
        ).all()
        
        for record in records:
            if record.clock_out and record.hours_worked() > 12:
                unusual_patterns.append(f"{employee.name} worked {record.hours_worked():.1f} hours on {record.clock_in.strftime('%Y-%m-%d')}")
    
    if unusual_patterns:
        insights.append(f"Unusual work patterns detected: {unusual_patterns[0]}" + 
                      (" and others" if len(unusual_patterns) > 1 else ""))
    
    return render_template('analytics.html',
        daily_hours=daily_hours,
        squad_hours=dict(squad_hours),
        location_data=top_locations,
        top_employees=top_employees,
        employee_avg_hours=employee_avg_hours,
        employee_last_active=employee_last_active,
        total_hours_all_time=round(total_hours_all_time, 2),
        avg_daily_hours=avg_daily_hours,
        top_squad=top_squad,
        underperforming_count=underperforming_count,
        underperforming_employees=underperforming_employees,
        employee_count=len(employees),
        squads=squads,
        insights=insights
    )

# Route to handle squad leader assignment
@app.route('/assign_squad_leader/<int:squad_id>', methods=['GET', 'POST'])
@login_required
def assign_squad_leader(squad_id):
    squad = Squad.query.get_or_404(squad_id)
    squad_employees = Employee.query.filter_by(squad_id=squad_id).all()
    
    if request.method == 'POST':
        leader_id = request.form.get('leader_id')
        if leader_id:
            squad.squad_leader_id = leader_id
            db.session.commit()
            flash(f'Squad leader assigned successfully!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('assign_squad_leader.html', squad=squad, employees=squad_employees)

app.jinja_env.globals.update(calculate_total_hours=calculate_total_hours)

# Create database tables and admin user if they don't exist
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('paula2025*')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

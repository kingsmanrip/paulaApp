from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

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

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
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
    
    # Get date range for current week (Monday to Sunday)
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    return render_template('dashboard.html', 
                          employees=employees,
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
        
        lines = data.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("ClockIn-"):
                # Process clock in data
                parts = line.split('employee: ')[1].split('location: ')
                employee_names = parts[0].strip()
                location_parts = parts[1].split('date: ')
                location = location_parts[0].strip()
                date_str = location_parts[1].strip()
                
                # Parse date
                try:
                    date_obj = datetime.strptime(date_str, '%B %d, %Y at %I:%M %p')
                except ValueError:
                    flash(f'Error parsing date: {date_str}')
                    continue
                
                # Process each employee
                for emp_name in employee_names.split(' '):
                    if not emp_name or emp_name in ["and"]:
                        continue
                    
                    # Try to find employee
                    employee = Employee.query.filter_by(name=emp_name).first()
                    if not employee:
                        employee = Employee(name=emp_name)
                        db.session.add(employee)
                        db.session.commit()
                    
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
                    
            elif line.startswith("ClockOut-"):
                # Process clock out data
                parts = line.split('employee: ')[1].split('location: ')
                employee_names = parts[0].strip()
                location_parts = parts[1].split('date: ')
                location = location_parts[0].strip()
                date_str = location_parts[1].strip()
                
                # Parse date
                try:
                    date_obj = datetime.strptime(date_str, '%B %d, %Y at %I:%M %p')
                except ValueError:
                    flash(f'Error parsing date: {date_str}')
                    continue
                
                # Process each employee
                for emp_name in employee_names.split(' '):
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
        
        flash('Data imported successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('bulk_import.html')

def calculate_total_hours(employee, start_date=None, end_date=None):
    query = TimeRecord.query.filter_by(employee_id=employee.id)
    
    if start_date:
        query = query.filter(TimeRecord.clock_in >= datetime.combine(start_date, datetime.min.time()))
    
    if end_date:
        query = query.filter(TimeRecord.clock_in <= datetime.combine(end_date, datetime.max.time()))
    
    records = query.all()
    total_hours = sum(record.hours_worked() for record in records)
    
    return round(total_hours, 2)

@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %I:%M %p'):
    if value:
        return value.strftime(format)
    return ""

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

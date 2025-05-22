# ALPHA CONTRACTING Employee Tracker

A comprehensive web-based application for tracking employee attendance, work hours, and locations with squad organization, performance analytics, and reporting features.

## Features

- Secure login system with ALPHA CONTRACTING branding
- Squad-based organization of employees
- Dashboard with squad and individual work hour summaries
- Automated performance insights with underperforming employee detection
- PDF report generation with customizable date ranges
- Analytics dashboard with visualizations and performance metrics
- Employee management
- Time record tracking (clock in/out)
- Location tracking and distribution analytics
- Daily, weekly, and total hour calculations
- Squad performance tracking and comparisons
- Bulk data import
- Mobile-friendly responsive design

## Login Credentials

- Username: `admin`
- Password: `paula2025*`

## How to Use

1. **Dashboard**: View summary of all squads and employees' work hours with automated insights
2. **Squad Overview**: See employees grouped by squads with squad performance metrics
3. **Employee Details**: Click on "Details" for any employee to see their complete work history
4. **Add Employee**: Add new employees to the system
5. **Add Record**: Manually add clock in/out records for employees
6. **Bulk Import**: Paste formatted data to import multiple clock in/out records at once
7. **Reports**: Generate PDF reports of employee hours for specific date ranges
8. **Analytics**: Access the analytics dashboard for visual performance metrics

## Squad Organization

Employees are organized into squads for better team management:

- **Employee1 Squad**: Core field team including Caleb Bryant, Aaron Mitchell, Seth James, Colton Poore, David Pool, and Shawn Beard
- **Employee8 Squad**: Secondary team including Jeramy Smith, Johnnie Roberts, Blake Hay, and Maurilio Galvez

Each squad displays:
- Aggregated squad hours (daily and weekly)
- Individual employee performance
- Member count and activity metrics

## Bulk Import Format

```
ClockIn- employee: Name1 Name2 Name3
location: Address
date: Month DD, YYYY at HH:MM AM/PM

ClockOut- employee: Name1 Name2 Name3
location: Address
date: Month DD, YYYY at HH:MM AM/PM
```

## Running the Application

### Development Mode
```bash
cd /root/employee_tracker
. venv/bin/activate
flask run --host=0.0.0.0
```

### Production Deployment
The application is deployed on Hostinger VPS (IP: 178.16.142.169) and accessible at:
https://alphainsight.site

The production deployment uses:
- Nginx as a reverse proxy with SSL
- Systemd service for 24/7 operation and automatic restarts
- Let's Encrypt SSL certificates

### Setting up as a Systemd Service
```bash
# Create the systemd service file
sudo nano /etc/systemd/system/employee-tracker.service

# Add the following content
[Unit]
Description=ALPHA CONTRACTING Employee Tracker
After=network.target

[Service]
User=root
WorkingDirectory=/root/employee_tracker
ExecStart=/root/employee_tracker/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable employee-tracker
sudo systemctl start employee-tracker
```

## System Requirements

- Python 3.6+
- Flask and Flask extensions (Flask-Login, Flask-SQLAlchemy, Flask-WeasyPrint)
- SQLite
- Gunicorn (for production)
- Nginx (for production)
- WeasyPrint dependencies (for PDF generation)
- Modern web browser

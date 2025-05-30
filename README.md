# ALPHA CONTRACTING Employee Tracker

A comprehensive web-based application for tracking employee attendance, work hours, and locations with squad organization, performance analytics, and reporting features.

## Features

- Secure login system with ALPHA CONTRACTING branding
- Squad-based organization of employees with squad leaders
- Clean dashboard showing employee work performance
- Performance insights section on the analytics page
- PDF report generation with customizable date ranges
- Advanced analytics dashboard with visualizations and performance metrics
- Employee management and assignment
- Time record tracking (clock in/out)
- Location tracking and distribution analytics
- Daily, weekly, and total hour calculations
- Squad performance tracking and comparisons
- Bulk data import with multi-line format support
- Mobile-friendly responsive design

## Login Credentials

- Username: `admin`
- Password: `paula2025*`

## How to Use

1. **Dashboard**: View squads and employees' work hours with assigned squad leaders
2. **Squad Overview**: See employees grouped by squads with phone numbers
3. **Squad Leader Management**: Assign or change squad leaders using the button next to each squad name
4. **Employee Details**: Click on "Details" for any employee to see their complete work history
5. **Add Employee**: Add new employees to the system
6. **Add Record**: Manually add clock in/out records for employees
7. **Bulk Import**: Paste formatted data to import multiple clock in/out records at once
8. **Reports**: Generate PDF reports of employee hours for specific date ranges
9. **Analytics**: Access the analytics dashboard for visual performance metrics and insights

## Squad Organization

Employees are organized into squads for better team management, with each squad identified by a phone number:

- **Employee1 (601-434-7661)**: Core field team including Caleb Bryant, Aaron Mitchell, Seth James, Colton Poore, David Pool, and Shawn Beard
- **Employee2 (601-610-2935)**: Team members assigned to this squad
- **Employee3 (601-610-2936)**: Team members assigned to this squad
- **Employee4 (601-610-2933)**: Team members assigned to this squad
- **Employee5 (601-610-2937)**: Team members assigned to this squad
- **Employee6 (601-610-2938)**: Team members assigned to this squad
- **Employee7 (601-610-2931)**: Team members assigned to this squad
- **Employee8 (601-610-2944)**: Secondary team including Jeramy Smith, Johnnie Roberts, Blake Hay, and Maurilio Galvez

### Squad Leadership

Each squad can have an assigned squad leader:
- Squad leaders are selected from members of that squad
- Leaders can be assigned or changed through the dashboard interface
- The squad leader's name appears under the squad name on the dashboard

### Employee Performance Tracking

Each employee card displays:
- Latest day's hours
- Weekly hours
- Total hours worked
- Access to detailed performance history

## Analytics and Insights

The Analytics page provides comprehensive performance metrics and visualizations:

- **Performance Insights**: Automated analysis highlighting top-performing squads, underperforming employees, inactive employees, and unusual work patterns
- **Productivity Trends**: Daily hours chart showing work patterns over time
- **Squad Performance**: Comparative analysis of squad productivity
- **Location Distribution**: Map of employee activity locations
- **Top Performers**: List of employees with highest average hours

Insights are automatically generated based on employee data and provide actionable intelligence for management decisions.

## Latest Time Records

As of May 26, 2025, the system includes the latest time records for the primary teams. Note how individual employee hours are tracked regardless of which squad they work with on a given day:

### May 30, 2025 - Six Teams in the Field

**Complete Time Records**
- Six full teams operating across Mississippi
- 34 employees clocked in at various locations
- 33 employees completed both clock-in and clock-out
- One employee (Antonio Jimenez) clocked in but did not clock out
- Teams operating in Meridian, Osyka, and Magee
- Half-day schedule for Caleb Bryant and James Jarrell's teams

### May 28, 2025 - Full Teams Back in Action

**Multiple Teams Across Mississippi**
- 6 teams working across different locations in Mississippi
- 33 employees in total logged hours today
- Teams in Meridian, Osyka, Magee, and Marion

### May 27, 2025 - No Activity

**Weather Event**
- All work stopped due to heavy rainfall
- No time records for this date
- Safety precaution to avoid hazardous conditions

### May 26, 2025 - Multiple Teams

**Marion MS Team**
- Clock In: 8:03 AM at 5449-5491 Fairground Dr, Marion MS 39342
- Clock Out: 1:02 PM at 5449-5491 Fairground Dr, Marion MS 39342
- Team members: James Jarrell, Thomas King, Seth Pope, Kyzer Revette, Richard Carter, Rodolfo Coronado
- Hours worked: 4 hours 59 minutes

**Forest-to-Hattiesburg Team**
- Clock In: 8:51 AM at 11065 MS-35, Forest MS 39074
- Clock Out: 6:51 PM at 85 Indian Ridge Rd, Hattiesburg MS 39401
- Team members: Willy Galvez, Eliseo Galvez
- Hours worked: 10 hours 0 minutes

### May 24, 2025 - Employee7 Squad First Day

**Forest MS Team (Cross-Squad Collaboration)**
- Clock In: 8:46 AM at 10679 MS-35, Forest MS 39074
- Clock Out: 5:30 PM at 4079-4205 MS-35, Forest MS 39074
- Team members: Caleb Bryant (Employee1), Rene Rivas, Jaime Garcia, Willy Galvez, Antonio Jimenez, Reynaldo Martinez, Maurilio Galvez
- Hours worked: 8 hours 44 minutes
- Special note: First day for Employee7 squad with Caleb Bryant (Employee1) providing supervision/training

### May 23, 2025

**Magee Team (Partial Employee1 Squad)**
- Clock In: 7:51 AM at 642 Ninth Ave NW, Magee MS 39111
- Clock Out: 2:18 PM at 201-299 Dolly Ln NW, Magee MS 39111
- Team members: Caleb Bryant, Colton Poore, Shawn Beard
- Hours worked: 6 hours 27 minutes

**Meridian Team (Partial Employee8 Squad)**
- Clock In: 8:46 AM at 3453 Grandview Ave, Meridian MS 39305
- Clock Out: 12:09 PM at I-20 W, Meridian MS 39307
- Team members: Jeramy Smith, Blake Hay, Maurilio Galvez
- Hours worked: 3 hours 23 minutes

### May 22, 2025

**Employee1 Squad (601-434-7661)**
- Clock In: 8:25 AM at 571 Simpson Hwy 149, Magee MS
- Clock Out: 4:35 PM at 149 Simpson Hwy 149, Magee MS
- Full team attendance: Caleb Bryant, Aaron Mitchell, Seth James, Colton Poore, David Pool, Shawn Beard

**Employee8 Squad (601-610-2944)**
- Clock In: 10:15 AM at 615-699 Cherry St NW, Magee MS
- Clock Out: 5:47 PM at Evelyn Gandy Pkwy, Hattiesburg MS
- Team members: Jeramy Smith, Johnnie Roberts, Blake Hay (no clock-out), Maurilio Galvez, Rodolfo Coronado

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

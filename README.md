# Employee Tracker

A web-based application for tracking employee attendance, work hours, and locations with squad organization.

## Features

- Secure login system
- Squad-based organization of employees
- Dashboard with squad and individual work hour summaries
- Employee management
- Time record tracking (clock in/out)
- Location tracking
- Daily, weekly, and total hour calculations
- Squad performance tracking
- Bulk data import
- Mobile-friendly responsive design

## Login Credentials

- Username: `admin`
- Password: `paula2025*`

## How to Use

1. **Dashboard**: View summary of all squads and employees' work hours
2. **Squad Overview**: See employees grouped by squads with squad performance metrics
3. **Employee Details**: Click on "Details" for any employee to see their complete work history
4. **Add Employee**: Add new employees to the system
5. **Add Record**: Manually add clock in/out records for employees
6. **Bulk Import**: Paste formatted data to import multiple clock in/out records at once

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

The application runs on port 5000. Access it at:
http://[server-ip]:5000

## System Requirements

- Python 3.6+
- Flask
- SQLite
- Modern web browser

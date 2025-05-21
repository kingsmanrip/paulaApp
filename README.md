# Employee Tracker

A web-based application for tracking employee attendance, work hours, and locations.

## Features

- Secure login system
- Dashboard with individual and team work hour summaries
- Employee management
- Time record tracking (clock in/out)
- Location tracking
- Daily, weekly, and total hour calculations
- Bulk data import
- Mobile-friendly responsive design

## Login Credentials

- Username: `admin`
- Password: `paula2025*`

## How to Use

1. **Dashboard**: View summary of all employees' work hours
2. **Employee Details**: Click on "Details" for any employee to see their complete work history
3. **Add Employee**: Add new employees to the system
4. **Add Record**: Manually add clock in/out records for employees
5. **Bulk Import**: Paste formatted data to import multiple clock in/out records at once

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

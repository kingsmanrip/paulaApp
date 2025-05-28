# Time Records SFTP Upload Instructions

## System Overview
I've set up an automated system that will:
1. Monitor the `/root/employee_tracker/uploads/time_records` folder for new .txt files
2. Process those files to extract time records in the standard format (ClockIn/ClockOut)
3. Add the records to the Employee Tracker database
4. Move processed files to a "processed" folder with timestamps

## How to Use with iPhone Shortcuts

### Setting Up Your iPhone Shortcut

1. **Create a New Shortcut** in the Shortcuts app
2. **Add Actions** to process your SMS:
   - "Get Messages" or "When I receive a message" as your trigger
   - "Extract Text from Input" to get the content
   - "Save File" action to save the text

3. **Configure the Save File Action**:
   - Set "Service" to "SFTP"
   - Enter the following connection details:
     - **Host**: 178.16.142.169 (your VPS IP)
     - **Port**: 22 (standard SFTP port)
     - **User**: root
     - **Password**: [your server password]
     - **Path**: /root/employee_tracker/uploads/time_records/
     - **Filename**: time_record_[Current Date].txt (use the "Current Date" variable)

4. **Test the Shortcut** with one of your time record SMS messages

### File Format Requirements

Your SMS messages should maintain this format for automatic processing:
```
ClockIn-
employee:
[Employee Names]
location:
[Location]
date:
[Date and Time]
ClockOut-
employee:
[Employee Names]
location:
[Location]
date:
[Date and Time]
```

## Testing the System

To test if the system is working:
1. Save a test file with the above format to the uploads folder
2. The file should disappear within a minute as it's processed
3. Check the log at `/root/employee_tracker/uploads/upload_processor.log`
4. Verify the records appear in your Employee Tracker dashboard

## Troubleshooting

If records aren't appearing in the system:
1. Check the log file for any errors
2. Verify employee names exactly match those in the database
3. Ensure the date format follows one of these patterns:
   - May 26, 2025 at 8:03 AM
   - May 26, 2025, 8:03 AM
   - 05/26/2025 8:03 AM
   - 2025-05-26 08:03

## Security Note

This setup uses SFTP which encrypts your data during transfer. However, if you're concerned about security:
1. Consider setting up a dedicated user instead of using root
2. Use key-based authentication instead of password
3. Restrict access to only the uploads folder

For additional assistance, please contact your system administrator.

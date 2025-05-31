#!/bin/bash

# Create a new crontab entry to run the backup script at 11 PM daily
(crontab -l 2>/dev/null; echo "0 23 * * * cd /root/employee_tracker && /usr/bin/python3 /root/employee_tracker/db_backup.py >> /root/employee_tracker/db_save_folder/backup.log 2>&1") | crontab -

echo "Database backup cron job has been set up to run daily at 11:00 PM."
echo "Backups will be saved in /root/employee_tracker/db_save_folder/ with timestamps."

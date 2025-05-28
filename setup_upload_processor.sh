#!/bin/bash

# Make script executable
chmod +x /root/employee_tracker/process_uploads.py

# Create systemd service file
cat > /etc/systemd/system/time-record-processor.service << EOL
[Unit]
Description=Time Record Upload Processor
After=network.target

[Service]
User=root
WorkingDirectory=/root/employee_tracker
ExecStart=/usr/bin/python3 /root/employee_tracker/process_uploads.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
systemctl daemon-reload
systemctl enable time-record-processor.service
systemctl start time-record-processor.service

echo "Time record processor service has been set up and started"

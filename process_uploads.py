#!/usr/bin/env python3
import os
import time
import logging
import sqlite3
import re
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='/root/employee_tracker/uploads/upload_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constants
UPLOAD_DIR = '/root/employee_tracker/uploads/time_records'
PROCESSED_DIR = '/root/employee_tracker/uploads/processed'
DB_PATH = '/root/employee_tracker/instance/employee_tracker.db'

# Create processed directory if it doesn't exist
if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

def parse_time_records(file_path):
    """Parse time records from a file in the standard SMS format."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split into clock-in and clock-out sections
    records = []
    current_record = {}
    current_section = None
    employee_names = []
    location = ""
    date_str = ""
    
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('ClockIn-'):
            # Start a new record
            current_section = 'clock_in'
            employee_names = []
            location = ""
            date_str = ""
        elif line.startswith('ClockOut-'):
            current_section = 'clock_out'
            employee_names = []
            location = ""
            date_str = ""
        elif line.startswith('employee:'):
            # Next lines will be employee names
            pass
        elif line.startswith('location:'):
            # Next lines will be location
            pass
        elif line.startswith('date:'):
            # Next line will be date
            pass
        elif current_section == 'clock_in' or current_section == 'clock_out':
            # Processing employee names, location, or date
            if 'employee:' in line:
                # Line contains employee info
                names = line.replace('employee:', '').strip()
                employee_names.append(names)
            elif any(location_indicator in line.lower() for location_indicator in ['street', 'ave', 'blvd', 'rd', 'ln', 'dr', 'way', 'ct', 'pl', 'hwy', 'st']):
                # Line likely contains location info
                location += line + " "
            elif re.match(r'.*\d{1,2}:\d{2}.*', line):
                # Line contains date and time
                date_str = line
                
                # Process this complete record
                if employee_names and location and date_str:
                    # Parse all individual employees
                    for emp_line in employee_names:
                        for emp_name in emp_line.split():
                            if emp_name and emp_name not in ['and']:
                                if current_record.get(emp_name) is None:
                                    current_record[emp_name] = {}
                                
                                if current_section == 'clock_in':
                                    current_record[emp_name]['clock_in'] = date_str
                                    current_record[emp_name]['location_in'] = location.strip()
                                elif current_section == 'clock_out':
                                    current_record[emp_name]['clock_out'] = date_str
                                    current_record[emp_name]['location_out'] = location.strip()
                                
                                # If we have a complete record, add it to records
                                if 'clock_in' in current_record.get(emp_name, {}) and 'clock_out' in current_record.get(emp_name, {}):
                                    records.append({
                                        'name': emp_name,
                                        'clock_in': current_record[emp_name]['clock_in'],
                                        'location_in': current_record[emp_name]['location_in'],
                                        'clock_out': current_record[emp_name]['clock_out'],
                                        'location_out': current_record[emp_name]['location_out']
                                    })
    
    return records

def insert_time_records(records):
    """Insert time records into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    inserted_count = 0
    
    for record in records:
        try:
            # First find the employee ID
            cursor.execute("SELECT id FROM employee WHERE name = ?", (record['name'],))
            result = cursor.fetchone()
            if not result:
                logging.warning(f"Employee not found: {record['name']}")
                continue
                
            employee_id = result[0]
            
            # Parse dates
            try:
                # Try various date formats that might come from SMS
                date_formats = [
                    '%B %d, %Y at %I:%M %p',  # May 26, 2025 at 8:03 AM
                    '%b %d, %Y at %I:%M %p',  # May 26, 2025 at 8:03 AM
                    '%B %d, %Y, %I:%M %p',    # May 26, 2025, 8:03 AM
                    '%b %d, %Y, %I:%M %p',    # May 26, 2025, 8:03 AM
                    '%m/%d/%Y %I:%M %p',      # 05/26/2025 8:03 AM
                    '%m-%d-%Y %I:%M %p',      # 05-26-2025 8:03 AM
                    '%Y-%m-%d %H:%M',         # 2025-05-26 08:03
                ]
                
                clock_in_dt = None
                clock_out_dt = None
                
                for fmt in date_formats:
                    try:
                        clock_in_dt = datetime.strptime(record['clock_in'], fmt)
                        break
                    except ValueError:
                        continue
                        
                for fmt in date_formats:
                    try:
                        clock_out_dt = datetime.strptime(record['clock_out'], fmt)
                        break
                    except ValueError:
                        continue
                
                if not clock_in_dt or not clock_out_dt:
                    logging.error(f"Could not parse dates for record: {record}")
                    continue
                    
                # Format for SQLite
                clock_in_str = clock_in_dt.strftime('%Y-%m-%d %H:%M:%S')
                clock_out_str = clock_out_dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Check if this record already exists to avoid duplicates
                cursor.execute("""
                    SELECT COUNT(*) FROM time_record 
                    WHERE employee_id = ? AND DATE(clock_in) = DATE(?)
                """, (employee_id, clock_in_str))
                
                if cursor.fetchone()[0] > 0:
                    logging.info(f"Record already exists for {record['name']} on {clock_in_dt.date()}")
                    continue
                
                # Insert the record
                cursor.execute("""
                    INSERT INTO time_record (employee_id, clock_in, clock_out, location_in, location_out)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    employee_id,
                    clock_in_str,
                    clock_out_str,
                    record['location_in'],
                    record['location_out']
                ))
                
                inserted_count += 1
                logging.info(f"Inserted record for {record['name']} on {clock_in_dt.date()}")
                
            except Exception as e:
                logging.error(f"Error parsing dates for {record['name']}: {e}")
                continue
                
        except Exception as e:
            logging.error(f"Error processing record for {record['name']}: {e}")
            continue
    
    conn.commit()
    conn.close()
    return inserted_count

def process_file(file_path):
    """Process a single time record file."""
    try:
        logging.info(f"Processing file: {file_path}")
        
        # Parse records from file
        records = parse_time_records(file_path)
        
        if not records:
            logging.warning(f"No valid records found in {file_path}")
            return False
            
        # Insert records into database
        inserted_count = insert_time_records(records)
        
        logging.info(f"Successfully processed {inserted_count} records from {file_path}")
        return True
        
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return False

def process_uploads():
    """Process all files in the upload directory."""
    for filename in os.listdir(UPLOAD_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # Process the file
            success = process_file(file_path)
            
            # Move to processed directory with timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_filename = f"{timestamp}_{filename}"
            processed_path = os.path.join(PROCESSED_DIR, new_filename)
            
            try:
                os.rename(file_path, processed_path)
                logging.info(f"Moved {filename} to {processed_path}")
            except Exception as e:
                logging.error(f"Error moving file {filename}: {e}")

def main():
    """Main function to run the upload processor."""
    logging.info("Starting upload processor")
    
    try:
        while True:
            process_uploads()
            time.sleep(60)  # Check for new files every minute
    except KeyboardInterrupt:
        logging.info("Upload processor stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error in upload processor: {e}")
        
if __name__ == "__main__":
    main()

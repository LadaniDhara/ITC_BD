import requests
import csv
import os
import paramiko
from scp import SCPClient
from datetime import datetime

# API URL
url = "https://api.tfl.gov.uk/Line/elizabeth/Status"

# Define file paths
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"elizabeth_status_{timestamp}.csv"
local_csv_path = r"C:\Users\anich\OneDrive\Desktop\ITC-class\project\ITC_BD\\" + csv_filename  # Save in the current directory

# HDFS Directory Path
HDFS_DIRECTORY = "/tmp/big_datajan2025/TFL"
hdfs_file_path = f"{HDFS_DIRECTORY}/{csv_filename}"

# Hadoop Server Credentials
hadoop_server = "18.170.23.150"  # Ensure this is correct
hadoop_user = "ec2-user"
ssh_key_path = r"C:\Users\anich\Downloads\test_key.pem"

# Fetch API response with error handling
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"❌ API Request Error: {e}")
    exit(1)

# Save data locally
try:
    with open(local_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Mode", "Status Severity", "Status Description", "Reason", "Service Type"])

        for line in data:
            line_id = line.get("id", "N/A")
            line_name = line.get("name", "N/A")
            mode = line.get("modeName", "N/A")

            status_severity = "N/A"
            status_description = "N/A"
            reason = "No reason provided"

            for status in line.get("lineStatuses", []):
                status_severity = status.get("statusSeverity", "N/A")
                status_description = status.get("statusSeverityDescription", "N/A")
                reason = status.get("reason", "No reason provided")

            service_type = "N/A"
            for service in line.get("serviceTypes", []):
                service_type = service.get("name", "N/A")

            writer.writerow([line_id, line_name, mode, status_severity, status_description, reason, service_type])

    print(f"✅ Data saved locally: {local_csv_path}")

except Exception as e:
    print(f"❌ Error saving data locally: {e}")
    exit(1)

# Transfer file to Hadoop Server using SCP
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hadoop_server, username=hadoop_user, key_filename=ssh_key_path)

    with SCPClient(ssh.get_transport()) as scp:
        remote_csv_path = f"/home/{hadoop_user}/{csv_filename}"
        scp.put(local_csv_path, remote_path=remote_csv_path)

    print(f"✅ File transferred to Hadoop Server: {remote_csv_path}")

except Exception as e:
    print(f"❌ Error transferring file to Hadoop Server: {e}")
    exit(1)

# Upload file to HDFS
try:
    command = f"hdfs dfs -mkdir -p {HDFS_DIRECTORY} && hdfs dfs -put -f {remote_csv_path} {hdfs_file_path}"
    stdin, stdout, stderr = ssh.exec_command(command)

    print(stdout.read().decode())  # Show HDFS output
    print(stderr.read().decode())  # Show any error messages

    print(f"✅ Data uploaded to HDFS: {hdfs_file_path}")

except Exception as e:
    print(f"❌ Error uploading file to HDFS: {e}")

finally:
    ssh.close()

import os
import requests
import json
import hashlib
import hmac
import base64
from datetime import datetime

# Retrieve variables from environment (set by Azure DevOps)
workspace_id = os.getenv('LAWorkspaceID')
workspace_key = os.getenv('LAWorkspaceKey')
log_type = "DriftDetectionLogs"
time_stamp_field = ""

app_folder = os.getenv('appFolder')
filtered_drift_report_file = os.getenv('filteredDriftReportFile')
build_definition_name = os.getenv('Build_DefinitionName')
build_id = os.getenv('Build_BuildId')

# Check if required variables are set
if not all([workspace_id, workspace_key, app_folder, filtered_drift_report_file, build_definition_name, build_id]):
    print("One or more required environment variables are missing.")
    exit(1)

# Read the filtered drift report
filtered_drift_report_path = os.path.join(app_folder, filtered_drift_report_file)
try:
    with open(filtered_drift_report_path, 'r') as file:
        filtered_drift_report_content = file.read()
except FileNotFoundError:
    print(f"Drift report file not found at path: {filtered_drift_report_path}")
    exit(1)

# Prepare the log entry
log_entry = {
    "DriftReport": filtered_drift_report_content,
    "PipelineName": build_definition_name,
    "BuildId": build_id,
    "TimeGenerated": datetime.utcnow().isoformat() + 'Z'  # ISO 8601 format
}

# Convert to JSON
json_data = json.dumps([log_entry])  # Wrapping log_entry in a list
content_length = len(json_data)

# Build the signature
method = "POST"
content_type = "application/json"
resource = "/api/logs"
rfc1123date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')  # RFC1123 format
x_headers = f"x-ms-date:{rfc1123date}"
string_to_hash = f"{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}"

# Encode the string to sign
bytes_to_hash = string_to_hash.encode('utf-8')

# Decode the Workspace Key from base64
key_bytes = base64.b64decode(workspace_key)

# Compute the HMAC-SHA256 hash
signature = base64.b64encode(hmac.new(key_bytes, bytes_to_hash, hashlib.sha256).digest()).decode('utf-8')

# Create the authorization header
authorization = f"SharedKey {workspace_id}:{signature}"

# Build the request
uri = f"https://{workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01"
headers = {
    "Content-Type": content_type,
    "Authorization": authorization,
    "Log-Type": log_type,
    "x-ms-date": rfc1123date,
    "time-generated-field": time_stamp_field
}

# Send the request
try:
    response = requests.post(uri, headers=headers, data=json_data)
    if response.status_code == 200:
        print("Data sent to Azure Monitor successfully.")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
except Exception as e:
    print(f"Failed to send data to Azure Monitor: {e}")
    raise e
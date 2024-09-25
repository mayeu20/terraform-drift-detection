import requests
import json
import os

# Retrieve variables from environment (set by Azure DevOps)
app_folder = os.getenv('appFolder')
filtered_drift_report_file = os.getenv('filteredDriftReportFile')
build_definition_name = os.getenv('Build_DefinitionName')
build_id = os.getenv('Build_BuildId')

# Check if required variables are set
if not all([app_folder, filtered_drift_report_file, build_definition_name, build_id]):
    print("One or more required environment variables are missing.")
    exit(1)

# Define the URI
uri = "https://" #Update with your MS Teams WebHook URL

# Construct the path to the drift report file
drift_report_file_path = os.path.join(app_folder, filtered_drift_report_file)

# Read the content of the drift report file
try:
    with open(drift_report_file_path, 'r') as file:
        drift_report_content = file.read()
except FileNotFoundError:
    print(f"Drift report file not found at path: {drift_report_file_path}")
    exit(1)

# Construct the payload
payload = {
    "title": "Terraform Drift Detected",
    "text": "Drift has been detected in the Application Stack's deployment. Please review the attached details.",
    "sections": [
        {
            "activityTitle": "Drift Report",
            "activitySubtitle": f"{build_definition_name} - Build {build_id}",
            "text": f"``{drift_report_content}``"
        }
    ]
}

# Convert the payload to JSON
payload_json = json.dumps(payload)

# Send the message to Microsoft Teams using the webhook
try:
    response = requests.post(uri, headers={'Content-Type': 'application/json'}, data=payload_json)
    if response.status_code == 200:
        print("Message sent to Microsoft Teams successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
except Exception as e:
    print(f"Failed to send message to Microsoft Teams: {e}")
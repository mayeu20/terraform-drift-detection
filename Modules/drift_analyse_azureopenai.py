from openai import AzureOpenAI
import os

# Initialize the Azure OpenAI client with environment variables for security
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),  # Azure OpenAI endpoint
    api_version="2023-07-01-preview",  # Updated API version
    api_key=os.getenv("AZURE_OPENAI_API_KEY")  # API Key from environment
    )

# Read the Terraform drift report
app_folder = os.getenv("APP_FOLDER")  # Environment variable for the app folder
drift_report_file = os.getenv("DRIFT_REPORT_FILE")  # Environment variable for drift report file

try:
    with open(f"{app_folder}/{drift_report_file}", "r") as file:
        terraform_plan_text = file.read()
except FileNotFoundError:
    print(f"Error: The file {drift_report_file} was not found in {app_folder}.")
    exit(1)

# Prepare the OpenAI prompt
prompt = f"""
You are a Terraform expert reviewing the output of a Terraform plan. I need you to extract all the infrastructure changes from the plan, including the resources affected, along with their pre- and post-apply states. Please exclude any tag changes.
The following is a Terraform plan output, detailing the upcoming changes to the infrastructure:
  + create new resources
  ~ update existing resources in place
  - destroy existing resources
  -/+ destroy and then create a replacement resource

For each resource, please provide:
The resource name.
The change (whether it will be created, updated, or deleted).
The pre-apply state of the resource.
The post-apply state of the resource.
Ensure that changes to tags are excluded. Format the output clearly with resources grouped by their change type (create, update, delete).
{terraform_plan_text}
"""

# Call Azure OpenAI to process the drift report using the updated API
try:
    response = client.chat.completions.create(
        model="gpt-35-turbo",  # Replace with the correct deployment name
        messages=[
            {"role": "system", "content": "You are an AI that processes Terraform plans."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.2
    )

# Extract the filtered result using `model_dump()`
    filtered_result = response.model_dump()['choices'][0]['message']['content'].strip()

    # Write the filtered result to a new file
    filtered_drift_report_file = os.getenv("FILTERED_DRIFT_REPORT_FILE")  # Environment variable for output file
    with open(f"{app_folder}/{filtered_drift_report_file}", "w") as filtered_file:
        filtered_file.write(filtered_result)
    print(filtered_result)

    print("Filtered drift report (without tags) has been successfully generated.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)
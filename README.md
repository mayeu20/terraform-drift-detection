# Azure Terraform Drift Detection Pipeline

This repository contains a fully automated pipeline for detecting and reporting infrastructure drift in **Terraform-managed** Azure environments. The solution leverages **Azure DevOps** and **Azure OpenAI GPT** to analyze Terraform plans, filter the results, and send notifications to stakeholders via email, Microsoft Teams, and Azure Monitor.

## Features

- **Automated Drift Detection**: Checks for discrepancies between Terraform-managed infrastructure and the desired state.
- **AI-Powered Drift Reporting**: Processes the Terraform plan using **Azure OpenAI GPT** to extract meaningful changes, excluding tag modifications.
- **Multi-Channel Notifications**: Sends drift reports to:
  - **Azure Monitor** for logging and monitoring.
  - **Microsoft Teams** for team collaboration.
  - **Email** for direct stakeholder notification.

## Repository Structure

terraform-drift-detection/
- Modules
	- send_email.py        			# Python script to send email notifications
	- drift_analyse_azureopenai.py  # Python script to process drift using Azure OpenAI
	- drift_send_to_msteams.py		# Python script to send to MS teams channel via WebHook
- azure-pipeline.yml       			# Azure DevOps Pipeline YAML
- README.md                    		# Documentation for the repository

## Getting Started

### Prerequisites

1. **Azure DevOps** with access to configure pipelines.
2. **Terraform** installed on your build agents.
3. **Azure OpenAI** service set up with the necessary API keys.
4. **SMTP Server** details for sending email notifications.
5. **Microsoft Teams** webhook URL for sending drift alerts to your Teams channel.

### Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mayeu20/terraform-drift-detection.git
   cd terraform-drift-detection
2. **Set up the Azure Pipeline**:
	Use the Pipelines/azure-pipeline.yml file to create a new pipeline in Azure DevOps.
3. **Configure Environment Variables**:
	Add the following environment variables in your Azure DevOps Library group:
	- AZURE_OPENAI_API_KEY
	- AZURE_OPENAI_API_BASE
 	- APP_FOLDER
  	- DRIFT_REPORT_FILE
   	- FILTERED_DRIFT_REPORT_FILE
   	- SMTP_USERNAME
   	- SMTP_PASSWORD
   	- TEAMS_WEBHOOK_URL
4. **Update the yaml file**:
	Update the values in the variables section under the Application-specific details as variables will need to be udpates.
	Update the Job and Display names on line 25 and 26.

### Usage

1. **Run the Pipeline**:
Trigger the Azure DevOps pipeline to automatically detect drift, analyze it using Azure OpenAI, and send the notifications.

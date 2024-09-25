import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# SMTP server details
smtp_server = "add your smtp server"
smtp_port = 25
smtp_username = os.getenv("SMTP_USERNMAE")  # Retrieve from environment variables
smtp_password = os.getenv("SMTP_PASSWORD")  # Retrieve from environment variables

# Email details
sender_email = "sender email" #To Be Updated
receiver_email = "receiver email address" #To Be Updated
subject = "Terraform Drift Report for Application XXXX"  #To Be Updated
drift_report_file = os.path.join(os.getenv("APP_FOLDER"), os.getenv("FILTERED_DRIFT_REPORT_FILE"))

# Read the drift report content
with open(drift_report_file, "r") as file:
    drift_report_content = file.read()

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Email body
body = f"""
Hello,

Please find below the details of the drift detected in the Application XXX infrastructure:

{drift_report_content}

Regards,
DevOps Team
"""
message.attach(MIMEText(body, "plain"))

# Attach the drift report file
with open(drift_report_file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(drift_report_file)}",
    )
    message.attach(part)

# Convert the message to a string
text = message.as_string()

# Enforce TLS 1.2 only
context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # Create a context using the general TLS protocol
context.options |= ssl.OP_NO_TLSv1  # Disable TLS 1.0
context.options |= ssl.OP_NO_TLSv1_1  # Disable TLS 1.1

try:
    # Connect to the SMTP server using TLS 1.2 only
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection with TLS 1.2
        server.ehlo()  # Can be omitted
        server.login(smtp_username, smtp_password)  # Login using SMTP credentials
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")

import os
import smtplib
from email.mime.text import MIMEText

def send_email_alert(student_id, name, email, programme, school):
    """Send academic probation alert emails to multiple stakeholders."""
    subject = "Academic Probation Alert"
    body = (
        f"Dear {name},\n\n"
        f"Your cumulative GPA has fallen below the threshold. Please contact your advisor immediately.\n"
        f"Programme: {programme}\n"
        f"School: {school}\n\n"
        f"Thank you,\nUniversity Administration."
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "enchantoalder@gmail.com"

    # Add recipients
    recipients = [
        email,  # Student email
        "darynnbrown@gmail.com",
        "enchantoalder@gmail.com"
    ]
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Adjust SMTP settings as needed
            server.login("enchantoalder@gmail.com", "rpjg lslg nawi hlze")  # Replace with real credentials
            server.sendmail(msg["From"], recipients, msg.as_string())
        print(f"Email alert sent to {email} and other stakeholders.")
    except Exception as e:
        print(f"Error sending email alert for {name} (ID: {student_id}): {e}")
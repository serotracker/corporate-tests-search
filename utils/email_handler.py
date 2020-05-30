import os
import smtplib
import ssl
from email.mime.text import MIMEText

from .search_group_handler import get_search_group


# SMTP setup
port = 465
context = ssl.create_default_context()
sender = 'iitbackendalerts@gmail.com'
recipients = ['abeljohnjoseph@gmail.com', 'can.serosurveillance.dev@gmail.com']  # Add additional email addresses here
password = os.getenv('GMAIL_PASS')


def send_email_complete():
    # Configure the full email body
    search_group = get_search_group()
    body = f"Hello,\n\nThe search for Group {search_group} has completed.\n\nSincerely,\nServer Alerts"
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender, password)

        msg = MIMEText(body)
        msg['Subject'] = f"Search for Group {search_group} has completed"
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        server.sendmail(sender, recipients, msg.as_string())

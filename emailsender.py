# email_sender.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, content):
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        print("SendGrid API-nyckel är inte satt. E-post kommer inte att skickas.")
        return

    message = Mail(
        from_email='din_email@exempel.com',
        to_emails='mottagare@exempel.com',
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("E-post skickad vid larm.")
    except Exception as e:
        print(f"Fel vid skickande av e-post: {e}")

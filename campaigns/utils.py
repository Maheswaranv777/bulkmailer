import os
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()

def send_email_mailjet(to_email, subject, html_content):
    mailjet = Client(
        auth=(os.getenv("MJ_APIKEY_PUBLIC"), os.getenv("MJ_APIKEY_PRIVATE")),
        version='v3.1'
    )
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "your_verified_sender@example.com",
                    "Name": "Your Company"
                },
                "To": [{"Email": to_email}],
                "Subject": subject,
                "HTMLPart": html_content
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()

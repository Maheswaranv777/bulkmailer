import csv
from datetime import datetime

def log_delivery(campaign_name, recipient_email, status, reason=None):
    with open('data/delivery_logs.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            campaign_name,
            recipient_email,
            status,
            reason or "",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])


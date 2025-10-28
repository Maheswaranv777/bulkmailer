import csv

class Recipient:
    def __init__(self, name, email, status):
        self.name = name
        self.email = email
        self.status = status

def load_recipients(file_path):
    recipients = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Subscription Status'] == 'Subscribed':
                recipients.append(Recipient(row['Name'], row['Email'], row['Subscription Status']))
    return recipients

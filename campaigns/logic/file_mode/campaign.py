import json
from datetime import datetime

class Campaign:
    def __init__(self, name, subject, content, scheduled_time, status):
        self.name = name
        self.subject = subject
        self.content = content
        self.scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
        self.status = status


def load_campaigns(file_path):
    with open(file_path) as f:
        raw = f.read()
        if not raw.strip():
            raise ValueError("❌ campaigns.json is empty!")
        data = json.loads(raw)
        return [Campaign(**c) for c in data]

def update_campaign_status(file_path, campaign_name, new_status):
    with open(file_path, "r+") as f:
        data = json.load(f)
        for c in data:
            if c['name'] == campaign_name:
                c['status'] = new_status
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
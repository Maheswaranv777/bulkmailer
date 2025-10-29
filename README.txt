Bulkmailer - Bulk Email Campaign Management System
===================================================

This is a flexible Django-based application for managing and sending bulk email campaigns using Mailjet.
The system supports two modes of execution:

1. **Django ORM Mode** – Uses PostgreSQL and Django Admin Dashboard with full database support.
2. **File Mode** – A lightweight mode that runs directly on CSV and JSON files without needing a database.

---------------------------------------------------
📁 PROJECT STRUCTURE
---------------------------------------------------

.
├── bulkmailer/               # Django project (settings, URLs, WSGI)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── campaigns/                # Main Django app
│   ├── models.py             # ORM Models: Campaign, Recipient, EmailLog
│   ├── views.py              # Dashboard, Create, Upload, and Detail views
│   ├── urls.py               # App-specific URL routing
│   ├── forms.py
│   ├── templates/campaigns/  # HTML templates
│   │   ├── dashboard.html
│   │   ├── create_campaign.html
│   │   ├── upload.html
│   │   └── detail.html
│   ├── logic/file_mode/      # File-based logic for no-DB mode
│   │   ├── mailjet_client.py
│   │   ├── scheduler.py
│   │   ├── campaign.py
│   │   ├── logger.py
│   │   └── recipient.py
│   └── migrations/
│
├── data/                     # File-mode storage
│   ├── recipients.csv
│   ├── campaigns.json
│   └── delivery_logs.csv
│
├── scheduler.py              # Sends scheduled campaigns using ORM
├── run_campaigns_file.py     # Runs campaigns using file mode
├── manage.py                 # Django project entry point
├── requirements.txt          # Python dependencies
└── README.txt                # Project documentation (this file)

---------------------------------------------------
⚙️ SETUP INSTRUCTIONS (ORM MODE)
---------------------------------------------------

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL
```sql
CREATE DATABASE bulkmailer;
CREATE USER bulkuser WITH PASSWORD 'bulkpass';
GRANT ALL PRIVILEGES ON DATABASE bulkmailer TO bulkuser;
```

### 4. Configure `.env` File
```
DB_NAME=bulkmailer
DB_USER=bulkuser
DB_PASSWORD=bulkpass
DB_HOST=localhost
DB_PORT=5432

MJ_APIKEY_PUBLIC=your_mailjet_public_key
MJ_APIKEY_PRIVATE=your_mailjet_private_key
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start the Server
```bash
python manage.py runserver
```

Visit in browser: http://127.0.0.1:8000/

- Dashboard: `/`
- Create Campaign: `/campaigns/create/`
- Upload Recipients: `/recipients/upload/`

---------------------------------------------------
✉️ MAILJET INTEGRATION
---------------------------------------------------

Configured in `mailjet_client.py`:

```python
def send_email(to_email, subject, html_content):
    mailjet = Client(
        auth=(os.getenv("MJ_APIKEY_PUBLIC"), os.getenv("MJ_APIKEY_PRIVATE")),
        version='v3.1'
    )
    data = {
        'Messages': [{
            "From": {"Email": "Mahesrocky96@gmail.com", "Name": "Sense7ai"},
            "To": [{"Email": to_email}],
            "Subject": subject,
            "HTMLPart": html_content
        }]
    }
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()
```

Install the SDK:
```bash
pip install mailjet-rest
```

---------------------------------------------------
⚡ RUNNING THE MAIL SCHEDULER (ORM MODE)
---------------------------------------------------

After creating campaigns and uploading recipients:

```bash
python scheduler.py
```

This script:
- Fetches scheduled campaigns
- Sends emails to subscribed recipients
- Logs delivery results
- Updates campaign status to "completed"

---------------------------------------------------
🪶 FILE MODE (NO DATABASE REQUIRED)
---------------------------------------------------

Run campaigns without using Django or PostgreSQL:

### Sample Files (`/data/`)

**recipients.csv**
```csv
name,email,subscription_status
User1,user1@yopmail.com,subscribed
User2,user2@yopmail.com,subscribed
```

**campaigns.json**
```json
[
  {
    "id": 1,
    "name": "Test Campaign",
    "subject": "🚀 Launch Offer",
    "content": "<h1>Hello User!</h1><p>This is our latest offer.</p>",
    "scheduled_time": "2025-10-29T16:00:00",
    "status": "scheduled"
  }
]
```

### Run file-mode sender:

```bash
python run_campaigns_file.py
```

Sends emails using Mailjet and logs results to `data/delivery_logs.csv`.

---------------------------------------------------
📦 REQUIREMENTS
---------------------------------------------------

```
Django>=4.2
psycopg2-binary
python-dotenv
mailjet-rest
```

Install with:
```bash
pip install -r requirements.txt
```

---------------------------------------------------
🕓 CRON JOB FOR AUTOMATION
---------------------------------------------------

To run the mail scheduler every 5 minutes:

```bash
*/5 * * * * cd /path/to/project && source venv/bin/activate && python scheduler.py
```

---------------------------------------------------
📊 TEST CAMPAIGN SAMPLE
---------------------------------------------------

- Name: Welcome Blast
- Subject: Welcome to Sense7AI
- Content: `<h1>Hi!</h1><p>Thanks for joining us.</p>`
- Scheduled time: (any time before `now`)
- Status: `scheduled`

Run:
```bash
python scheduler.py
```

---------------------------------------------------
✅ READY TO USE!
---------------------------------------------------

You now have a full-featured, mail-capable bulk campaign manager.

Author: Maheswaran  
Email: Mahesrocky96@gmail.com  
Company: Sense7AI  
Date: October 2025
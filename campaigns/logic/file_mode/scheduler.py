from datetime import datetime

from bulkmailer.campaigns.models import EmailLog
from .recipient import Recipient, load_recipients
from .campaign import Campaign, load_campaigns, update_campaign_status
from .logger import log_delivery
from .mailjet_client import send_email

def run_campaigns():
    print("✅ run_campaigns() started")

    try:
        campaigns = load_campaigns('data/campaigns.json')
        print(f"📦 Loaded {len(campaigns)} campaigns")
    except Exception as e:
        print(f"❌ Failed to load campaigns: {e}")
        return

    try:
        recipients = load_recipients('data/recipients.csv')
        print(f"👥 Loaded {len(recipients)} recipients")
    except Exception as e:
        print(f"❌ Failed to load recipients: {e}")
        return

    for campaign in campaigns:
        print(f"\n🔍 Checking campaign: {campaign.name}")
        print(f"   Status: {campaign.status}")
        print(f"   Scheduled for: {campaign.scheduled_time}")
        print(f"   Current time : {datetime.now()}")

        if campaign.status == 'Scheduled' and campaign.scheduled_time <= datetime.now():
            print(f"🚀 Running campaign: {campaign.name}")
            update_campaign_status('data/campaigns.json', campaign.name, 'In Progress')

        
            for recipient in recipients:
                try:
                    code, response = send_email(recipient.email, campaign.subject, campaign.content)
                    status = 'Sent' if code == 200 else 'Failed'
                    reason = None if code == 200 else str(response)
                except Exception as e:
                    status = 'Failed'
                    reason = str(e)

                log_delivery(campaign.name, recipient.email, status, reason)
                print(f"{status} → {recipient.email}")
                if reason:
                    print(f"   ↳ Reason: {reason}")

            update_campaign_status('data/campaigns.json', campaign.name, 'Completed')
            print(f"✅ Campaign completed: {campaign.name}")
        else:
            print("⏩ Skipping (not scheduled or already completed)")
            
    
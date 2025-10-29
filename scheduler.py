# from bulkmailer.campaigns.models import Campaign, EmailLog, Recipient
# from campaigns.logic.file_mode.mailjet_client import send_email  # import your function
# from django.utils.timezone import now

# def run_due_campaigns():
#     due_campaigns = Campaign.objects.filter(status='scheduled', scheduled_time__lte=now())

#     for campaign in due_campaigns:
#         recipients = Recipient.objects.filter(subscription_status='subscribed')
#         campaign.status = 'in_progress'
#         campaign.save()

#         for recipient in recipients:
#             try:
#                 status_code, response = send_email(
#                     to_email=recipient.email,
#                     subject=campaign.subject,
#                     html_content=campaign.content
#                 )
#                 if status_code == 200:
#                     EmailLog.objects.create(
#                         campaign=campaign,
#                         recipient=recipient,
#                         status='sent'
#                     )
#                 else:
#                     EmailLog.objects.create(
#                         campaign=campaign,
#                         recipient=recipient,
#                         status='failed',
#                         failure_reason=str(response)
#                     )
#             except Exception as e:
#                 EmailLog.objects.create(
#                     campaign=campaign,
#                     recipient=recipient,
#                     status='failed',
#                     failure_reason=str(e)
#                 )

#         campaign.status = 'completed'
#         campaign.save()




import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulkmailer.settings')
django.setup()



from campaigns.models import Campaign, EmailLog, Recipient
from campaigns.logic.file_mode.mailjet_client import send_email
from django.utils.timezone import now

#### for test drve ######

# campaign = Campaign.objects.get(name="October Promo")
# campaign.status = "scheduled"
# campaign.scheduled_time = now()  # make it due right now
# campaign.save()

###########

def run_due_campaigns():
    due_campaigns = Campaign.objects.filter(status='scheduled', scheduled_time__lte=now())
    print(f"Found {due_campaigns.count()} due campaigns.")

    for campaign in due_campaigns:
        print(f"Running campaign: {campaign.subject}")
        recipients = Recipient.objects.filter(subscription_status='subscribed')
        print(f"Recipients found: {recipients.count()}")

        campaign.status = 'in_progress'
        campaign.save()

        for recipient in recipients:
            print(f"→ Sending to: {recipient.email}")
            try:
                status_code, response = send_email(
                    to_email=recipient.email,
                    subject=campaign.subject,
                    html_content=campaign.content
                )
                if status_code == 200:
                    EmailLog.objects.create(
                        campaign=campaign,
                        recipient=recipient,
                        status='sent'
                    )
                else:
                    EmailLog.objects.create(
                        campaign=campaign,
                        recipient=recipient,
                        status='failed',
                        failure_reason=str(response)
                    )
            except Exception as e:
                EmailLog.objects.create(
                    campaign=campaign,
                    recipient=recipient,
                    status='failed',
                    failure_reason=str(e)
                )

        campaign.status = 'completed'
        campaign.save()

if __name__ == "__main__":
    run_due_campaigns()

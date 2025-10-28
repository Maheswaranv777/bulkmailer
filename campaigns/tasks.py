from django.utils import timezone
from .models import Campaign, Recipient, EmailDeliveryLog
from .utils import send_email_mailjet

def execute_due_campaigns():
    now = timezone.now()
    campaigns = Campaign.objects.filter(status='Scheduled', scheduled_time__lte=now)

    for campaign in campaigns:
        campaign.status = 'In Progress'
        campaign.save()

        recipients = Recipient.objects.filter(status='Subscribed')
        for recipient in recipients:
            try:
                code, response = send_email_mailjet(
                    recipient.email,
                    campaign.subject,
                    campaign.content
                )
                status = 'Sent' if code == 200 else 'Failed'
                reason = None if code == 200 else str(response)
            except Exception as e:
                status = 'Failed'
                reason = str(e)

            EmailDeliveryLog.objects.create(
                campaign=campaign,
                recipient=recipient,
                status=status,
                failure_reason=reason
            )

        campaign.status = 'Completed'
        campaign.save()

import csv
from io import TextIOWrapper
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from .models import Campaign, Recipient, EmailLog
from .forms import CampaignForm, RecipientUploadForm

def dashboard(request):
    campaigns = Campaign.objects.all()
    data = []
    for c in campaigns:
        sent = c.emaillog_set.filter(status='sent').count()
        failed = c.emaillog_set.filter(status='failed').count()
        data.append({'campaign': c, 'sent': sent, 'failed': failed})
    return render(request, 'campaigns/dashboard.html', {'data': data})


def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    logs = EmailLog.objects.filter(campaign=campaign)
    return render(request, 'campaigns/detail.html', {'campaign': campaign, 'logs': logs})

def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CampaignForm()
    return render(request, 'campaigns/create_campaign.html', {'form': form})

def upload_recipients(request):
    if request.method == 'POST':
        form = RecipientUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
            reader = csv.DictReader(file)

            for raw_row in reader:
                row = {k.strip().lower().replace(' ', '_'): v.strip() for k, v in raw_row.items()}

                if 'email' not in row:
                    continue  # skip bad rows

                Recipient.objects.update_or_create(
                    email=row['email'],
                    defaults={
                        'name': row.get('name', ''),
                        'subscription_status': row.get('subscription_status', 'subscribed').lower()
                    }
                )
            return redirect('dashboard')
    else:
        form = RecipientUploadForm()
    return render(request, 'campaigns/upload.html', {'form': form})



def send_campaigns():
    campaigns = Campaign.objects.filter(status='scheduled', scheduled_time__lte=now())
    for campaign in campaigns:
        campaign.status = 'in_progress'
        campaign.save()
        recipients = Recipient.objects.filter(subscription_status='subscribed')
        for recipient in recipients:
            try:
                send_mail(
                    campaign.subject,
                    campaign.content,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email],
                    fail_silently=False,
                )
                EmailLog.objects.create(campaign=campaign, recipient=recipient, status='sent')
            except Exception as e:
                EmailLog.objects.create(campaign=campaign, recipient=recipient, status='failed', failure_reason=str(e))
        campaign.status = 'completed'
        campaign.save()

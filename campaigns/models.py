from django.db import models

class Recipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=15, choices=[('Subscribed', 'Subscribed'), ('Unsubscribed', 'Unsubscribed')])

class Campaign(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('Draft', 'Draft'), ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'), ('Completed', 'Completed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

class EmailDeliveryLog(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Sent', 'Sent'), ('Failed', 'Failed')])
    failure_reason = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

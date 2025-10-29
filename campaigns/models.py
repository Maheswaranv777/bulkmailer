from django.db import models

class Recipient(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('subscribed', 'Subscribed'),
        ('unsubscribed', 'Unsubscribed'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    subscription_status = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='subscribed')

    def __str__(self):
        return self.email

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

from django.contrib import admin
from .models import Campaign, Recipient, EmailLog

admin.site.register(Campaign)
admin.site.register(Recipient)
admin.site.register(EmailLog)

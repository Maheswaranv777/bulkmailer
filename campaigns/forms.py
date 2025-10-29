from django import forms
from .models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'subject', 'content', 'scheduled_time', 'status']

class RecipientUploadForm(forms.Form):
    file = forms.FileField()

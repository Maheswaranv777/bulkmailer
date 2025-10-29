from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('campaigns/create/', views.create_campaign, name='create_campaign'),
    path('campaigns/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('recipients/upload/', views.upload_recipients, name='upload_recipients'),
]

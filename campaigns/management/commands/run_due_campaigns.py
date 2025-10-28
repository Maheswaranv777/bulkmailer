from django.core.management.base import BaseCommand
from campaigns.tasks import execute_due_campaigns

class Command(BaseCommand):
    help = 'Run due email campaigns from PostgreSQL'

    def handle(self, *args, **kwargs):
        execute_due_campaigns()
        self.stdout.write(self.style.SUCCESS('✅ Campaigns executed'))

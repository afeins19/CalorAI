# this script will delete all log history from a specified user 

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dailylog.models import DailyLog  

class Command(BaseCommand):
    help = 'Clears all daily logs for a specified user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user whose logs are to be cleared')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "%s" does not exist' % username))
            return
        
        # Delete all DailyLog entries for this user
        logs = DailyLog.objects.filter(user=user)
        log_count = len(logs)
        logs.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully cleared {log_count} daily logs for user "{username}"'))

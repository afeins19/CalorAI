from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dailylog.models import DailyLog

class Command(BaseCommand):
    help = 'Displays daily logs for users'

    def add_arguments(self, parser):
        # Optional: add arguments to command to filter by username or date
        parser.add_argument('--username', type=str, help='Username to filter the logs')
        parser.add_argument('--date', type=str, help='Date to filter the logs, format YYYY-MM-DD')

    def handle(self, *args, **options):
        username = options['username']
        date = options['date']
        logs_query = DailyLog.objects.all()

        if username:
            try:
                user = User.objects.get(username=username)
                logs_query = logs_query.filter(user=user)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR('User not found'))
                return
        
        if date:
            from datetime import datetime
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                logs_query = logs_query.filter(date=date_obj)
            except ValueError:
                self.stdout.write(self.style.ERROR('Date format should be YYYY-MM-DD'))
                return

        if not logs_query.exists():
            self.stdout.write('No logs found for the given criteria.')
        else:
            for log in logs_query:
                total_calories = log.breakfast_calories + log.lunch_calories + log.dinner_calories
                self.stdout.write(f"{log.user.username} - {log.date}: Breakfast {log.breakfast_calories} cal, Lunch {log.lunch_calories} cal, Dinner {log.dinner_calories} cal | Total={total_calories}")

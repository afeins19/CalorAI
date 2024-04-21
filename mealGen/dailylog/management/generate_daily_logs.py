# this script generates a history of daily logs for a valid registered user. 

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User 
from datetime import timedelta, date 
import random 
from dailylog import DailyLog

class Command(BaseCommand): 
    help = "Generates a specified number of daily logs for a valid user. [python manage.py generate_daily_logs <username> <No. days to generate>]"

    def add_arguments(self, parser): # lets us specify the user and the number of days we want to populate 
        parser.add_argument('username', type=str, help='Username of valid and registered user.')
        parser.add_argument('days', type=int, help='Number of days of history that will be generated.')

    def handle(self, *args, **options):
        # setting passed-in args 
        username = options['username']
        days = options['days']

        try: # finding the user if valid 
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' Does not exist."))
            return 

        start_date = date.today() - timedelta(days=days)
        end_date = date.today()

        # loop from start date (given in arg to this command) to the current date 
        for curdate in (start_date+timedelta(n) for n in range((end_date-start_date).days)):
            DailyLog.objects.create(
                user=user,
                date=curdate,
                breakfast_calories=random.randint(200, 500),
                breakfast_fat=random.randint(10, 15),
                breakfast_carbs=random.randint(30, 60),
                breakfast_protein=random.randint(10, 20),
                lunch_calories=random.randint(500, 800),
                lunch_fat=random.randint(20, 30),
                lunch_carbs=random.randint(60, 90),
                lunch_protein=random.randint(25, 35),
                dinner_calories=random.randint(400, 700),
                dinner_fat=random.randint(15, 25),
                dinner_carbs=random.randint(50, 80),
                dinner_protein=random.randint(20, 30),
                breakfast_time='08:00:00',
                lunch_time='13:00:00',
                dinner_time='19:00:00'
            )
        
        self.stdout.write(self.style.SUCCESS(f"Successfully Generated {days} of logs for '{username}'"))




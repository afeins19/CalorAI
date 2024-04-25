# this script generates a history of daily logs for a valid registered user. 

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User 
from datetime import timedelta, date 
import random 
import os 
import sys
import django 

# setting up the environment to do db calls without the server up 
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealgen.settings')
django.setup()


from dailylog.models import DailyLog
from core.models import UserProfile
import re

# commands to generate synthetic data 
class Command(BaseCommand): 
    help = "Generates a specified number of daily logs for a valid user. [python manage.py generate_daily_logs <username> <No. days to generate>]"

    def add_arguments(self, parser): # lets us specify the user and the number of days we want to populate 
        parser.add_argument('username', type=str, help='Username of valid and registered user.')
        parser.add_argument('days', type=int, help='Number of days of history that will be generated.')
        parser.add_argument('n_correlates', type=int, help='Number of features to correlate with target.')
        parser.add_argument('p_miss_target', type=float, help='Probability (.25<p<.75) that a users miss their calorie target on a given day')


    def handle(self, *args, **options):
        # setting passed-in args 
        username = options['username']
        days = options['days']
        n_correlates = options['n_correlates']
        p_miss_target = options['p_miss_target']
        calorie_goal = None 

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            calorie_goal = profile.daily_calorie_goal

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
            return

        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"UserProfile does not exist for user '{username}'."))
            return
        
        # select features to correlate based on n_correlates 
        features = [ 'breakfast_fat', 'breakfast_carbs', 'breakfast_protein',
                     'lunch_fat', 'lunch_carbs', 'lunch_protein',
                     'dinner_fat', 'dinner_carbs', 'dinner_protein'] # add meal skips later 
                                                                     # add meal time changes later 
        correlates = random.sample(features, n_correlates) 
        
        if len(correlates) > 0:
            print(f"Correlates ({len(correlates)}): {correlates}")

            # set scalar increases based on feature type (cal, fat, carb, protein, time)
            f_types = ['fat', 'carbs', 'protein', 'time']
            # creating a string to match feature types with the randomly selected ones
            re_types = re.compile('|'.join(re.escape(f) for f in f_types))
            # searchable string of selected correlated features 
            corr_str = str("".join(correlates))

            # see which types the selected features fall under
            selected_types = set(re_types.findall(corr_str))

            # fat=9cal/g, carb=4cal/g, protein=4cal/g

        start_date = date.today() - timedelta(days=days)
        end_date = date.today()

        days_cal_goal_missed=0 # counts total number of days calorie goal not achieved 

        # loop from start date (given in arg to this command) to the current date 
        for cur_date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
            # init daily macro sums to zero
            macro_sums = {'fat': 0, 'carbs': 0, 'protein': 0}

            # if curdate is a day where the target is missed
            if random.uniform(0.0,1.0) <= p_miss_target:
                days_cal_goal_missed+=1
                percent_increase = random.uniform(0.1, 0.25)
                for macro in ['fat', 'carbs', 'protein']:
                    if any(macro in corr for corr in correlates):
                        base_amount = int((0.3 * calorie_goal) / (4 if macro != 'fat' else 9)) # fat has 9 cals/gram 
                        macro_sums[macro] = base_amount * (1 + percent_increase)

            # calc todays total calories
            todays_calories = sum(macro_sums[macro] * (4 if macro != 'fat' else 9) for macro in macro_sums)
            meal_calories = todays_calories // 3

            # create the DailyLog entry
            DailyLog.objects.create(
                user=user,
                date=cur_date,
                breakfast_calories=meal_calories,
                breakfast_fat=macro_sums['fat'],
                breakfast_carbs=macro_sums['carbs'],
                breakfast_protein=macro_sums['protein'],
                lunch_calories=meal_calories,
                lunch_fat=macro_sums['fat'],
                lunch_carbs=macro_sums['carbs'],
                lunch_protein=macro_sums['protein'],
                dinner_calories=meal_calories,
                dinner_fat=macro_sums['fat'],
                dinner_carbs=macro_sums['carbs'],
                dinner_protein=macro_sums['protein'],
                breakfast_time='08:00:00',
                lunch_time='13:00:00',
                dinner_time='19:00:00'
            )

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully generated {days} days of logs for '{username}'."))
        print(f"Correlate Types: {selected_types}")
        print(f"P(TargetMissed)={p_miss_target}")
        print(f"Days Calorie Goal Missed={days_cal_goal_missed}")



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

        try: # finding the user if valid 
            user = User.objects.get(username=username)
            print(f"USER={username}")
            if not user:
                print("USER NOT FOUND")
                return 
            
            user_id = user.pk
            print(f"USER_ID={user_id}")
            # if user exists get the calorie goal 
             
            profile = UserProfile.objects.filter(user=user).first()
            calorie_goal = profile.daily_calorie_goal

            if not profile:
                print("Profile Not Found!")
            calorie_goal = profile.daily_calorie_goal

            print(calorie_goal)
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' Does not exist."))
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

            print(f"Correlate Types: {selected_types}")
            print(f"P(TargetMissed)={p_miss_target}")

            # standard percentages for macros for daily intake 
            standard_carbs = 0.3
            standard_fat, standard_protein = 0.3

            # fat=9cal/g, carb=4cal/g, protein=4cal/g

        start_date = date.today() - timedelta(days=days)
        end_date = date.today()

        # loop from start date (given in arg to this command) to the current date 
        for curdate in (start_date+timedelta(n) for n in range((end_date-start_date).days)):

            # start a daily log entry builder 
            daily_log_entry = {feature : None for feature in features}
        
            # see if we exceed the calorie goal by today 
            if random.random() <= p_miss_target: 
                percent_increase = random.random(.1, .25)
                per_meal_macro_grams = {"carb" : (standard_carbs * calorie_goal) // 4,
                                     "protein" : (standard_protein * calorie_goal) // 4,
                                     "fat" : (standard_fat * calorie_goal) // 9}
                
                # modify vals based on type 
                for correlate in correlates: 
                    num_meals=3 # modify later to handle meal skips 
                    if re.match(correlate, "carb"): 
                        per_meal_macro_grams['carb'] =  int(per_meal_macro_grams['carb'] * (1 + percent_increase)) // num_meals

                    if re.match(correlate, "protein"):
                        per_meal_macro_grams['protein'] =  int(per_meal_macro_grams['protein'] * (1 + percent_increase)) // num_meals

                    if re.match(correlate, "fat"):
                        per_meal_macro_grams['fat'] = int(per_meal_macro_grams['fat'] * (1 + percent_increase)) // num_meals

                    total_daily_calories = sum(list(per_meal_macro_grams.values()))
                    
            DailyLog.objects.create(
                user=user,
                date=curdate,

                breakfast_calories=total_daily_calories//3,
                breakfast_fat=per_meal_macro_grams['fat'],
                breakfast_carbs=per_meal_macro_grams['carbs'],
                breakfast_protein=per_meal_macro_grams['protein'],

                lunch_calories=total_daily_calories//3,
                lunch_fat=per_meal_macro_grams['fat'],
                lunch_carbs=per_meal_macro_grams['carbs'],
                lunch_protein=per_meal_macro_grams['protein'],

                dinner_calories=total_daily_calories//3,
                dinner_fat=per_meal_macro_grams['fat'],
                dinner_carbs=per_meal_macro_grams['carbs'],
                dinner_protein=per_meal_macro_grams['protein'],

                breakfast_time='08:00:00',
                lunch_time='13:00:00',
                dinner_time='19:00:00'
            )
        
        self.stdout.write(self.style.SUCCESS(f"Successfully Generated {days} of logs for '{username}'"))




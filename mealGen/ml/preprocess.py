# pulling in data from django ORM and performing some ml preprocessing on it 

import sys
import os
import django
from django.db.models import F
import pandas as pd 

# setting up the environment to do db calls without the server up 
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealgen.settings')
django.setup()

# KEEP THIS BELOW ENVIRONMENT PATH SETTING!!!!!!!!
from dailylog.models import DailyLog
from core.models import UserProfile

# loading in the data and returning a pandas df 
def load_daily_log_data(user_id=None):
    # pull in the data from db 
    if user_id:
        db_query = DailyLog.objects.filter(user_id=user_id).values()
        profile = UserProfile.objects.filter(user_id=user_id).first()
        calorie_goal = profile.daily_calorie_goal
    else:
        db_query = DailyLog.objects.all().values() # returns list of everything in the db 
        calorie_goal = 2000 # random default for empty db testing  

    if db_query:
        df = pd.DataFrame(list(db_query))

        # add users calorie goal to the df 
        df['calorie_goal'] = calorie_goal 
        print(f"Loaded columns: {df.columns}\n")
        return df
    return None 


# sums calories from all meals and sets the total_daily_calories col to this sum
def calculate_daily_calories(df):
    cal_cols = ['breakfast_calories', 'lunch_calories', 'dinner_calories']
    df['total_daily_calories'] = df[cal_cols].sum(axis=1)
    print(f"Calculated Daily Calories...")
    return df

# calculates the percentage of total calories for the day that each meal makes up 
def calculate_meal_percentages(df):
    cal_cols = ['breakfast_calories', 'lunch_calories', 'dinner_calories']

    for col in cal_cols:
        pct_col_str = col + '_pct' # generating the new name of the percent feature 
        df[pct_col_str] = df[col] / df['total_daily_calories'].replace(0,1)

    # fill days where user didnt log (total daily calories = 0)
    df.fillna(0, inplace=True)

    print(f"Calculated Meal Percentages...")

    return df 

# creates new cols that round the meal times to the nearest hour 
# also performs categorical encoding on them 
def encode_meal_times(df):
    time_cols = ['breakfast_time', 'lunch_time', 'dinner_time']

    # categorize times based on time category
    def categorize_time(t):
        if pd.isna(t):
            return "Skipped"

        hour = t.hour
        if 5 <= hour < 10:
            return "morning"
        elif 10 <= hour < 12:
            return "midday"
        elif 14 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 24:
            return "evening"
        else:
            return "night"

    for t in time_cols:
        time_str = t+'_cat' 
        df[time_str] = pd.to_datetime(df[t], format='%H:%M:%S', errors='coerce').apply(categorize_time) 

    print(f"Encoded Meal Times...")
    return df 

def encode_skipped_meals(df):
    time_cols = ['breakfast_time', 'lunch_time', 'dinner_time']

    for t in time_cols:
        time_str = t+'_skipped'
        df[time_str] = df[t].isnull().astype(int) # binary encode if meal was skipped or not 

    print(f"Encoded Skipped Meals...")
    return df 

# calculates the number of calories that the user went over/under their goal 
def calculate_over_under(df):
    df['calorie_diff'] = df['total_daily_calories'] - df['calorie_goal']
    print(f"Calculated Calorie Over-Under...")
    return df 

# T/F if users daily calories are within +- theshold of their goal
def met_calorie_goal(df, calorie_threshold=100): 
    df['met_cal_goal'] = (df['calorie_diff'].abs() <= calorie_threshold)
    print(f"Encoded Calorie Goal Attainment...")
    return df 

def preprocess_data(user_id=None):
    # chain the preprocessing operations 
    df = load_daily_log_data(user_id)

    if df is not None:
        print()
        df = calculate_daily_calories(df)
        df = calculate_meal_percentages(df)
        df = encode_meal_times(df)
        df = encode_skipped_meals(df)
        df = calculate_over_under(df)
        df = met_calorie_goal(df)

        return df 
    return None 

# run script as standalone 
if __name__ == '__main__': 
    print("Processing Data...")
    df = preprocess_data()

    if df is not None: 
        print("\nSucess!")
        print(f"Shape: {df.shape}\n")
        #print(df[:5])
    else:
        print("User Has No Log Entries.")
# pulling in data from django ORM and performing some ml preprocessing on it 

import sys
import os
import django
from django.db.models import F

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # add root dir to the script 
sys.path.append(f"mealGen")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealgen.settings')
django.setup()


from dailylog.models import DailyLog
import pandas as pd 
# setting up the environment to do db calls without the server up 

# loading in the data and returning a pandas df 
def load_daily_log_data():
    db_query = DailyLog.objects.all().values() # pull in the data from db 
    df = pd.DataFrame(list(db_query))
    print(f"Loaded columns: {df.columns}")
    return df

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

def preprocess_data():
    # chain the preprocessing operations 
    df = load_daily_log_data()
    df = calculate_daily_calories(df)
    df = calculate_meal_percentages(df)
    df = encode_meal_times(df)
    df = encode_skipped_meals(df)
    print(df.head())
    return df 

# run script as standalone 
if __name__ == '__main__': 
    print("Processing Data...")
    df = preprocess_data()
    
    if df is not None: 
        print("\nSucess!\n")
        print(df[:2])
    else:
        print("ERROR")
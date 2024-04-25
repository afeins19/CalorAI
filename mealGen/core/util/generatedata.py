import csv
import random
from datetime import datetime, timedelta

# generate random diet data
# synthetically insert correlations with target 
# n_corellations -> number of features to corellate with target 
# p_miss_target -> probability that target wont be met on a given day 
def generate_diet_data(start_date, num_days, n_correlates=0, p_miss_target=.5):
    data = []
    # raw user features
    """ ['breakfast_calories',
       'breakfast_fat', 'breakfast_carbs', 'breakfast_protein',
       'lunch_calories', 'lunch_fat', 'lunch_carbs', 'lunch_protein',
       'dinner_calories', 'dinner_fat', 'dinner_carbs', 'dinner_protein',
       'breakfast_time', 'lunch_time', 'dinner_time']"""
    
    # select features to correlate based on n_correlates 
    features = ['date', 
                'breakfast_calories', 'breakfast_fat', 'breakfast_carbs', 'breakfast_protein',
                'lunch_calories', 'lunch_fat', 'lunch_carbs', 'lunch_protein',
                'dinner_calories', 'dinner_fat', 'dinner_carbs', 'dinner_protein',
                'breakfast_time', 'lunch_time', 'dinner_time']
    
    correlates = random.sample(n_correlates, features) 

    if len(correlates) > 0:
        print(f"Correlates ({len(correlates)}): {correlates}")
    
    for _ in range(num_days):
        day = {
            "Date": start_date.strftime('%Y-%m-%d'),
        }
        data.append(day)
        start_date += timedelta(days=1)  # move to the next day
    return data



# write data to CSV
def write_to_csv(filename, data):
    fieldnames = ["Date", "Calories", "Carbs", "Fat", "Protein", "Exercise Level"]
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


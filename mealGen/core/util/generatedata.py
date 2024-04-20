import csv
import random
from datetime import datetime, timedelta

# generate random diet data
def generate_diet_data(start_date, num_days):
    data = []
    for _ in range(num_days):
        day = {
            "Date": start_date.strftime('%Y-%m-%d'),
            "Calories": random.randint(1500, 3000),
            "Carbs": random.randint(200, 400),
            "Fat": random.randint(50, 100),
            "Protein": random.randint(50, 150),
            "Exercise Level": random.randint(0, 5)
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


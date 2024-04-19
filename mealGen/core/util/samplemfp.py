import json
import os
# Correct the file path if necessary. The example uses Windows path conventions.
file_path = r'C:\Users\aaron\Projects\classWork\CMPSC445\calorai\OptimumMealGenerator\mealGen\core\userdata\FoodWithAdditionalNutritionalInformation.json'
print("Does the file exist?", os.path.exists(file_path))
with open(file_path, 'r') as f:
    data = json.load(f)  # Use json.load() to read JSON from a file object
    print(data)
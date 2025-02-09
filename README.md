# CalorAI

# Goal 

Given a users daily food-log data. This program will analyze trends in the data and determine if there are any correlations between them and the user not meeting their desired health goals. This program should highlight specific behaviors that the user may have which impede their calorie intake goals.  

**Target**: `met_calorie_goal`
- the models are trained to predict whether or not the user met his or her calorie goal on a given day given their data. 

# Project Structure 

1. Core App
    Models: User Profile, User Health Goals (Daily Calorie Target)
    Utilities: Helper functions -> `/util`

2. ML App (e.g., data_analysis)

    ML Models: XGBoost, RandomForest
    Data Preprocessing: Custom Scripts in `/ml`
    Analysis: Core analysis and processing logic
    Result Storage: Models or methods for storing analysis results.

3. Scaling and Preprocessing
    - Standard Scaler
    - balanced_classes (Random Forest)

5. API App (e.g., api)

    Endpoints: API views or viewsets exposing data and functionalities.
    Serializers: Data serialization for API responses.
    Authentication and Permissions: API-specific auth and access control.

6. Frontend App (e.g., frontend) 

    Templates: Django templates for the frontend.
    Static Files: CSS, html

# Main Filles

### Data & Models 
- **Preprocessing File**: `mealGen/ml/preprocess.py`

- **Model Generation File**: `mealGen/ml/generate_models.py`

- **Synthetic Data Generator**: `mealGen/dailylog/management/commands/generate_daily_logs.py`

- **Clearing User Logs**: `mealGen/dailylog/management/commands/clear_daily_logs.py`

### Django Backend

- **Views for core functionalitys**: `mealGen/core/views.py`

- **Views for daily logs and insights**: `mealGen/dailylog/views.py`

# User Creation

### Signing Up
To fully utilize the predictive features of the Calorie Intake Prediction Model, you'll need to create an account on our platform. This account will allow you to save your dietary inputs, view predictions, and track your progress over time.

#### Steps to Sign Up
1. **Navigate to the Sign-Up Page**: Open your web browser and go to the sign-up page at `http://localhost:8000/signup`.

2. **Fill Out the Registration Form**: Provide the necessary information such as your username, email address, and password. The form may also ask for additional information depending on the requirements of the application.

3. **Submit Your Details**: After filling out the form, submit your details by clicking the 'Sign Up' button at the bottom of the form. If there are any issues with the information you've provided, you'll receive error messages to correct them.

4. **Log In to Your Account**: Once you're registered, click `log in` on the homepage and enter you credentials.

5. **Enter Health Data**: you must click the `edit profile` link at the top nav-bar. The information entered there is crucial for the models to function properly.

# Installation 

### CalorAI Installation 
1. Clone this Repository to your desire location
2. Move to this directory: `/mealGen` (a file called `manage.py` should be located there)

### Poetry 
poetry is the package manager used for this program. To quickly download all the necessary libraries to your machine, we recommend using poetry. 

1. Open in a terminal and make sure python is installed with `python --version`
2. now run `pip install poetry` (pip is pythons package manager)
3. to install all the required packages, run the following command: `poetry install` and wait for package downloads to complete
4. now run `poetry shell` to activate the virtual environment

# Commands 
below is a quick start list of commands for proper use of this site.

- Starting the webserver locally: `python manage.py runserver` (ensure you are in the directory where `manage.py` is located)
- Stopping the webserver: `cntrl+c`

whens starting the site, the following should display in the terminal:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 26, 2024 - 12:57:57
Django version 5.0.4, using settings 'mealgen.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

# Demo Credentials
For the purposes of demonstration and testing, we have created a test user for generating synthetic data for (instructions given below). This users information already comes preloaded in the project database. To login as this user, please enter the credentials given below: 

*username:* test_user 

*password*: 12345 

### Synthetic Data Creation 

After logging in with these credentials. You will be able to make further daily log entries for meals as this user. Note that you must be logged in to create daily log entries and 
the site will not allow you to create any until you are a verified user that has been logged in. For this demonstartion, we have written a script that will automatically add log entries to this users history. This script is found at: `mealGen/dailylog/management/generate_daily_logs.py`. 

1. First clear their current history with this command: `python manage.py clear_daily_logs <username>`
2. Generate a new log history: `python manage.py generate_daily_logs <username> <days> <n_correlates> <p_miss_target>`

- `username`: username of a registered user
- `days`: the number of days to generate logs for the user 
- `n_correlates`: the number of features to artificailly correlate with the target 
- `p_miss_target`: probability that the user misses the target on any given day

*note: to avoid overfitting, we recommend setting the n_correlates value to atleast 8. Otherwise the data will not be complex enough and will suffer from overfitting.*

# Machine Learning Pipeline 

The models are trained to learn from the user data as well as our generated features. When satisfactory metrics are obtained, we extract the feature importances for that model and rank them. This is what we will present to the user. Essentially, the goal is to show what behaviors contributed most to the model predicting whether or not they would exceed a calorie goal for any given day. 

```
USER=test_user, CALORIE GOAL=1700
Loaded columns: Index(['id', 'user_id', 'profile_id', 'date', 'breakfast_calories',      
       'breakfast_fat', 'breakfast_carbs', 'breakfast_protein',
       'lunch_calories', 'lunch_fat', 'lunch_carbs', 'lunch_protein',
       'dinner_calories', 'dinner_fat', 'dinner_carbs', 'dinner_protein',
       'breakfast_time', 'lunch_time', 'dinner_time', 'calorie_goal'],
      dtype='object')

Calculated Daily Calories...
Calculated Meal Percentages...
Dropped column: breakfast_time_cat
Dropped column: lunch_time_cat
Dropped column: dinner_time_cat
Encoded Meal Times...
Encoded Skipped Meals...
Calculated Calorie Over-Under...
Encoded Calorie Goal Attainment...
[preprocess] Dropped Column: breakfast_time
[preprocess] Dropped Column: lunch_time
[preprocess] Dropped Column: dinner_time

Final Columns
        id
        user_id
        profile_id
        date
        breakfast_calories
        breakfast_fat
        breakfast_carbs
        breakfast_protein
        lunch_calories
        lunch_fat
        lunch_carbs
        lunch_protein
        dinner_calories
        dinner_fat
        dinner_carbs
        dinner_protein
        calorie_goal
        breakfast_calories_pct
        lunch_calories_pct
        dinner_calories_pct
        breakfast_time_cat_morning
        lunch_time_cat_night
        dinner_time_cat_evening
        breakfast_time_skipped
        lunch_time_skipped
        dinner_time_skipped
        calorie_diff
        met_cal_goal
Total=28

Data Split and Scaled...
DATA SHAPES:
X_train_scaled (140, 26)
X_test_scaled (35, 26)
y_train (140,)
y_test (35,)

User Data Loaded...
Random Forest Model Trained...
XGBoost Model Trained...
Models Trained...

Predicting with RandomForestC...
Predictions Made...

Predicting with XGBClassifier...
Predictions Made...

Random Forest:
[False False False False False False False False False  True False  True
 False  True False False False False False False False False False False
 False False False  True False False False False False  True False]

XGBoost:
[0 0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0]

Calculating Model Metrics...
Random Forest Metrics: {'accuracy': 1.0, 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0}

Calculating Model Metrics...
XGBoost Metrics: {'accuracy': 1.0, 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0}     
Getting Feature Importances for Model: RandomForestC
Getting Feature Importances for Model: XGBClassifier

Random Forset Feature Importances: [('lunch_calories', 0.12784953278229114), ('breakfast_calories', 0.10708837544024359), ('breakfast_protein', 0.09816381718604922)]

XGBoost Feature Importances: [('breakfast_calories', 0.9939034), ('id', 0.006096599), ('lunch_time_skipped', 0.0)]

Generating Plots...

Generating Plot for RandomForest...
Plot Saved...

Generating Plot for XGBoost...
Plot Saved...

Encoding plot: CalorAI/mealGen/static/images/randomforest_feature_importance_plot.png...
Plot Encoded...

Encoding plot: CalorAI/mealGen/static/images/xgboost_feature_importance_plot.png...
Plot Encoded...
```

### Steps
1. Data is pulled from the database (SQLite) and brought into our data preprocessing script (`ml/preprocess.py`)

2. a data frame is created and populated with the user's data

3. the following preprocessing steps are applied - this includes the feature engineering to add more data to our dataset:

- calculate daily calories (used for deriving other statistics but will be dropped)
- Calculate Meal Percentages
- Categorical encoding of meal times into times of day 
- Binary encode if a meal was skipped
- Calculate the amount the user's calorie goal is missed or exceeded
- Binary 
- Drop raw datetime columns (sklearn cannot handle those)

4. The data is split and sacled in the `split_scale()` function of `generate_models.py`. We standardize the data using Scikit-learn's `StandardScalar()`. Standardization applies the following function to each entry in the row: 

$$Z = \frac{(X - \mu)}{\sigma}$$

we then split into testing and training sets using Scikit-learn's `train_test_split()`. Crucially we pass in the parameter `stratify=y` which balances the sets based on our target variable: `calorie_goal_met`. 

5. The final dataset is returned to the `model_results_view()` in `core/views` and we then feed the data to the models. 

6. Model Predictions are returned and saved. 

7. The models metrics are evaluated to get an understanding of their predictive power. We calculate the following:

- Accuracy
- Recall
- Precission 
- F1  

8. We generate plots of the feature importances with repsect to each other. This is done for each model. These plots are then saved as `.png` files and procssed into base64 format for display in the html.

# Conclusion 
Below are some of the example plots that were generated by our models. Given that our model metrics are good, we can reasonably infer that these features contribute to the user not meeting his or her calorie goals. 

### RandomForest Model 
![Alt text](mealGen/randomforest_feature_importance_plot.png)

# Possible Improvements 

**Possible Overfitting** 
Currently The models obtain perfect score across all of our metrics. We believe this is due to the rather basic way our synthetic data generation script creates artificail correlations in the data. Experimenting with the data, we found that the modles began performing adequatley after roughly 10 days of log history. The best performing model with the most reasonable feature importances turend out to be the Random Forest Classifier. XGBoost consistently chose the same features in almost all cases, with one feature dominating the importance rating.

**Covariance Matrix**
to get a more detailed understanding of the features and how they interact with each other. Creating a covariance matrix would be a useful endevour for us. 

**Real-World Data**
To get a better understanding of model performance, we would like for real-world users to trial our app and have the models operate on real user logs. 










# CalorAI
given a users daily food-log data. This program will analyze trends between the data within a history of the user health logs and determine if there are any correlations between them and the user not meeting their desired health goals. 

 Structure
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












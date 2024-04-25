# Demonstration

For a sample demonstration of this application, you may log in as a demo user (credentials given below). This user will have an account with a weight loss goal and a pre-populated 
history of daily log entries for meals. 

*username:* username 
*password*: 12345 

After logging in with these credentials. You will be able to make further daily log entries for meals as this user. Note that you must be logged in to create daily log entries and 
the site will not allow you to create any until you are a verified user that has been logged in. For this demonstartion, we have written a script that will automatically add 2 months of daily log entries to this users history. This script is found at: `mealGen/dailylog/management/generate_daily_logs.py`. 

# Commands 

to give the user a prepopulated history of daily logs. Use the following commands 

1. First clear their current history with this command: `python manage.py clear_daily_logs <username>`
2. Generate a new log history: `python manage.py generate_daily_logs <username> <days> <n_correlates> <p_miss_target>`
    - `username`: username of a registered user 
    - `days`: the number of days to generate logs for the user 
    - `n_correlates`: the number of features to artificailly correlate with the target 
    - `p_miss_target`: probability that the user misses the target on any given day 



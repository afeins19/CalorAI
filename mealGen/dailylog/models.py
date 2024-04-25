from django.db import models
from django.contrib.auth.models import User
from core.models import UserProfile
import datetime
#import times 

# Create your models here.

class DailyLog(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) # tie to a particular user 
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='daily_logs', null=True)
    date = models.DateField()

    # dietary attributes for breakfast  
    breakfast_calories = models.IntegerField(default=0)
    breakfast_fat = models.IntegerField(default=0)
    breakfast_carbs = models.IntegerField(default=0)
    breakfast_protein = models.IntegerField(default=0)

    # dietary attributes for lunch  
    lunch_calories = models.IntegerField(default=0)
    lunch_fat = models.IntegerField(default=0)
    lunch_carbs = models.IntegerField(default=0)
    lunch_protein = models.IntegerField(default=0)

    # dietary attributes for dinner  
    dinner_calories = models.IntegerField(default=0)
    dinner_fat = models.IntegerField(default=0)
    dinner_carbs = models.IntegerField(default=0)
    dinner_protein = models.IntegerField(default=0)

    # meal times 
    breakfast_time = models.TimeField(null=True, blank=True) # null lets us skip meals
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)

    @property
    def user_calorie_goal(self):
        return self.profile.daily_calorie_goal

    def total_calories(self):
        return self.breakfast_calories + self.lunch_calories + self.dinner_calories
    
    def total_carbs(self):
        return self.breakfast_carbs + self.lunch_carbs + self.dinner_carbs
    
    def total_fat(self): 
        return self.breakfast_fat + self.lunch_fat + self.dinner_fat 
    
    def total_protein(self):
        return self.breakfast_protein + self. lunch_protein + self.dinner_protein
    
    def average_time_between_meals(self): 
        log_times = []
        # get all non-null meal times in a list
        if self.breakfast_time:
            times.append(datetime.combine(self.date, self.breakfast_time))
        if self.lunch_time:
            times.append(datetime.combine(self.date, self.lunch_time))
        if self.dinner_time:
            times.append(datetime.combine(self.date, self.dinner_time))

        # average interval between consecutive meal times
        if len(log_times) < 2:
            return None  # Not enough data to compute an average

        # sort times just in case they were not added in order
        times.sort()
        total_interval = timedelta()
        for i in range(1, len(log_times)):
            total_interval += times[i] - log_times[i - 1]

        avg_interval = total_interval / (len(log_times) - 1)
        return avg_interval

    def __str__(self):
        return f"{self.user.username}'s daily log for {self.date}"
    
    @property 
    def is_goal_met(self):
        # returns a true if the user met calorie goals, and false if not (within specified range)
        calorie_goal = self.user

    def __str__(self):
        return f"{self.user.username}'s log for {self.date}"

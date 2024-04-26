from django.db import models
from django.contrib.auth.models import User

from cryptography.fernet import Fernet # handling password encryption
# from dotenv import load_dotenv, set_key
#from env_generator import generate_key_and_update_env

import os 

# Create your models here.

class UserProfile(models.Model):
    """Holds the user's account information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    dietary_preferences = models.CharField(max_length=100)
    daily_calorie_goal = models.IntegerField(default=2000) 


class UserHealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    data_category = models.CharField(max_length=100, db_index=True)

    # raw JSON of the user's data
    data = models.JSONField()

class UserHealthGoal(models.Model):
    """User defined fitness attributes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    daily_calorie_goal = models.IntegerField(help_text="Daily Calorie Goal (log entries within 5 percent of this goal will count)", null=True)
    current_weight = models.IntegerField()
    target_weight = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.current_weight and self.target_weight:
            weight_delta = str(abs(self.current_weight - self.target_weight))

            if self.current_weight > self.target_weight:
                verb = "lose"
            elif self.current_weight < self.target_weight:
                verb = "gain"    

            return f"{self.user.username}'s goal is to {verb} {weight_delta} lbs."

        else:
            return f"{self.user.username} has no health goals yet."
        

        

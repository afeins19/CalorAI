from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DailyLog(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) # tie to a particular user 
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
    breakfast_time = models.TimeField(null=True, blank=True) # null lets us skip mea
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)

    def total_calories(self):
        return self.breakfast_calories + self.lunch_calories + self.dinner_calories
    
    def total_carbs(self):
        return self.breakfast_carbs + self.lunch_carbs + self.dinner_carbs
    
    def total_fat(self): 
        return self.breakfast_fat + self.lunch_fat + self.dinner_fat 
    
    def total_protein(self):
        return self.breakfast_protein + self. lunch_protein + self.dinner_protein
    
    def average_time_between_meals(self): 
        #@TODO: Compute time between each meal (consider skipped meals too )
        pass

    def __str__(self):
        return f"{self.user.username}'s log for {self.date}"

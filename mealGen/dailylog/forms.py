from django import forms
from .models import DailyLog
from django.contrib.auth.models import User

class DailyLogform(forms.ModelForm):
    class Meta:
        model = DailyLog

        fields = [
            'date',
            'breakfast_calroies', 'breakfast_fat', 'breakfast_carbs', 'breakfast_protein',
            'lunch_calories', 'lunch_fat', 'lunch_carbs', 'lunch_protein',
            'dinner_calories', 'dinner_fat', 'dinner_carbs', 'dinner_protein'
            'breakfast_time', 'lunch_time', 'dinner_time']

        widgets = {
            'date' : forms.DateInput(attrs={'type' : 'date'}),
            'breakfast_time' : forms.TimeInput(attrs={'type' : 'time'}, required=False),
            'lunch_time' : forms.TimeInput(attrs={'type' : 'time'}, required=False), 
            'dinner_time' : forms.TimeInput(attrs={'type' : 'time'}, required=False),
        }


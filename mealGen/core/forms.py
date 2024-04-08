from django import forms
from .models import HealthGoal

class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['target_value', 'current_value', 'start_date', 'end_date']

from django import forms
from .models import UserHealthData, UserHealthGoal
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAPICredentials

class SignUpForm(UserCreationForm):
    # signing in the form 
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    # logging in the user 
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = UserHealthGoal
        fields = ['current_weight', 'target_weight', 'daily_calorie_goal', 'start_date', 'end_date']


class UserAPICredentialsForm(forms.ModelForm):
    # lets the user input their MFP credentials 
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = UserAPICredentials
        fields = ['email', 'username']


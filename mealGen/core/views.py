from django.shortcuts import render, redirect
from .forms import HealthGoalForm
from .models import UserHealthGoal

from django.contrib.auth.views import LoginView
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate

from .forms import UserAPICredentialsForm
from .models import UserAPICredentials

# Create your views here.


def home(request):
    # homepage 
    return render(request, 'core/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Redirect to a home page or other page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def add_goal(request):
    # 
    if request.method == 'POST':
        form = HealthGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user 
            goal.save()
            
            # @TODO RETURN USER TO SOMEWHERE 
            # return redirect()

        # user is requesting to fill out the HealthGoalForm 
        else: 
            form = HealthGoalForm()
        return render(request, 'add_goal.html', {'form' : form})

def add_mfp_credentials(request):
    if request.method == 'POST':
        form = UserAPICredentialsForm(request.POST)
        
        if form.is_valid():
            mfp_credentials = form.save(commit=False) # holds data in memory but doesn save so we can link our app user
            mfp_credentials.user = request.user 
            mfp_credentials.password = form.cleaned_data['password'] # set encrypted password
            mfp_credentials.save()
            return redirect('')
    else:
        form = UserAPICredentialsForm() # return blank form 

    return render(request, 'core/add_mfp_credentials.html', {'form' : form}) 


def list_user_health_goals(request):
    # get the current users health goals 
    user_health_goals = UserHealthGoal.objects.filter(user=request.user)

    # pass to template 
    return render(request, 'list_user_health_goals.html', {'health_goals' : health_goals})




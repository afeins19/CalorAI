from django.shortcuts import render
from .forms import HealthGoalForm
from .models import UserHealthGoal

# Create your views here.

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
    
def list_user_health_goals(request):
    # get the current users health goals 
    user_health_goals = HealthGoal.objects.filter(user=request.user)

    # pass to template 
    return render(request, 'list_user_health_goals.html', {'health_goals' : health_goals})




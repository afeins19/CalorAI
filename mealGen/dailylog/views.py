from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DailyLogform

# Create your views here.

@login_required # requires user to be logged in for this to work
def add_daily_log(request):
    if request.method == 'POST': # user submits a filled out form 
        form = DailyLogform(request.POST)

        if form.is_valid(): # all required fields have the correct input 
            daily_log = form.save(commit=False)
            daily_log.user = request.user # associate this log with a given user 
            daily_log.save() 

            return redirect('daily_log_success') # redirect to a page to notify user of successful log operation 
        
    else:
        form = DailyLogform() # prepare an empty DailyLogForm() for the user 
        return render(request, 'dailylog/add_daily_log.html', {'form' : form})
        

def daily_log_success(request):
    return render(request, 'dailylog/log_success.html')


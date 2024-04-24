from django.shortcuts import render, redirect
from .forms import HealthGoalForm
from .models import UserHealthGoal

from django.contrib.auth.views import LoginView
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate

# imports from daillylog 
from dailylog.models import DailyLog

# ml modules 
from ml import generate_models as gm
from ml.preprocess import preprocess_data
from ml.make_plots import make_and_save_plot, to_base64

# plots 
import matplotlib as plt 
import seaborn as sns
from io import BytesIO
import base64 

#from .forms import UserAPICredentialsForm
#from .models import UserAPICredentials

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
            raw_password = form.cleaned_data.get('password')
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
            
            return render(request, '') # back to home page 

        # user is requesting to fill out the HealthGoalForm 
        else: 
            form = HealthGoalForm()
        
    return render(request, 'add_goal.html', {'form' : form})


def list_user_health_goals(request):
    # get the current users health goals 
    user_health_goals = UserHealthGoal.objects.filter(user=request.user)

    # pass to template 
    return render(request, 'list_user_health_goals.html', {'health_goals' : user_health_goals})

def model_results_view(request):
    user_id = request.user.id
    df = preprocess_data(user_id=user_id)
    target = 'met_cal_goal'

    if df is not None and 'met_cal_goal' in df.columns:
        # split and scale 
        data = gm.split_scale(df=df, target=target)

        if data:
            # train models
            random_forest = gm.train_random_forest(data['X_train_scaled'], data['y_train'])
            xgb = gm.train_xgboost(data['X_train_scaled'], data['y_train'])

            # make predictions 
            random_forest_predicitons = random_forest.predict(data['X_test_scaled'])
            xgb_predictions = xgb.predict(data['X_test_scaled'])

            # evaluate model performance 
            random_forest_metrics = gm.get_model_metrics(y_true=df[target], y_pred=random_forest_predicitons)
            xgb_metrics = gm.get_model_metrics(y_true=df[target], y_pred=xgb_predictions)

            # generate and save importance plots
            features = df.drop(columns=[target]).columns
            gm.make_and_save_plot(features, random_forest.feature_importances_,
                                  "Random Forest Feature Importance", "Random Forest", "rf_feature_importance.png")
            gm.make_and_save_plot(features, xgb.feature_importances_,
                                  "XGBoost Feature Importance", "XGBoost", "xgb_feature_importance.png")

            # convert plots to b64
            rf_plot_base64 = gm.to_base64('static/images/rf_feature_importance.png')
            xgb_plot_base64 = gm.to_base64('static/images/xgb_feature_importance.png')

            # hand-off to html 
            return render(request, 'model_results.html', {
                'rf_plot': rf_plot_base64,
                'rf_metrics' : random_forest_metrics,
                'xgb_plot': xgb_plot_base64,
                'xgb_metrics' : xgb_metrics
            })
    return render(request, 'error.html', {'message': 'Data not available or insufficient.'})



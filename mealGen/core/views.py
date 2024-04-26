from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserHealthGoal, UserProfile

from django.contrib.auth.views import LoginView
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

# imports from daillylog 
from dailylog.models import DailyLog

# ml modules 
from ml import generate_models as gm
from ml.preprocess import preprocess_data, get_col_data_types
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

@login_required
def model_results_view(request):
    user_id = request.user.id
    df = preprocess_data(user_id=user_id)
    df_log_entry_dates = df['date']

    # droping date col from df
    df = df.drop('date', axis=1)

    target = 'met_cal_goal'
    
    if df is not None:
        print(f"[view -> generate_models] Making Predictions for user: [{request.user.username}]")
        
        # split and scale 
        data = gm.split_scale(df=df, target=target)

        if data:
            print(f"\nUser Data Loaded...")
            # train models
            random_forest = gm.train_random_forest(data['X_train_scaled'], data['y_train'])
            xgb = gm.train_xgboost(data['X_train_scaled'], data['y_train'])
            print("Models Trained...")

            # make predictions 
            random_forest_predictions = gm.make_predictions(random_forest, data['X_test_scaled'])
            xgb_predictions = gm.make_predictions(xgb, data['X_test_scaled'])
            print("\nRandom Forest:")
            print(random_forest_predictions)
            print("\nXGBoost:")
            print(xgb_predictions)

            # evaluate performance
            features = df.drop(columns=[target]).columns

            random_forest_metrics = gm.get_model_metrics(y_true=data['y_test'], y_pred=random_forest_predictions)
            print("Random Forest Metrics:", random_forest_metrics)

            xgb_metrics = gm.get_model_metrics(y_true=data['y_test'], y_pred=xgb_predictions)
            print("XGBoost Metrics:", xgb_metrics)

            random_forest_ft_importances = gm.get_feature_importances(model=random_forest, feature_names=features)
            xgb_ft_importances = gm.get_feature_importances(model=xgb, feature_names=features)
            print(f"\nRandom Forset Feature Importances: {random_forest_ft_importances[:3]}")
            print(f"\nXGBoost Feature Importances: {xgb_ft_importances[:3]}")

            # formating feature importances for sending to hbar plot 
            rfc_plot_data = {
                "feature_importances" : [feature for feature, _ in random_forest_ft_importances][:5],
                "importance_values" : [val for _, val in random_forest_ft_importances][:5]}

            xgb_plot_data = {
                "feature_importances": [feature for feature, _ in xgb_ft_importances][:5],
                "importance_values": [val for _, val in xgb_ft_importances][:5]}
            
            # generate and save importance plots
            print(f"\nGenerating Plots...")
            rfc_plot_data = {
                "feature_importances": [feature for feature, _ in random_forest_ft_importances][:5],
                "importance_values": [val for _, val in random_forest_ft_importances][:5]}

            xgb_plot_data = {
                "feature_importances": [feature for feature, _ in xgb_ft_importances][:5],
                "importance_values": [val for _, val in xgb_ft_importances][:5]}
            
            rfc_path = gm.make_and_save_hbar_plot(
                x_label=rfc_plot_data['importance_values'],
                y_label=rfc_plot_data['feature_importances'],
                model_name='RandomForest',
                file_path='static/images'
            )

            xgb_path = gm.make_and_save_hbar_plot(
                x_label=xgb_plot_data['importance_values'],
                y_label=xgb_plot_data['feature_importances'],
                model_name='XGBoost',
                file_path='static/images'
            )

            # convert plots to b64
            rf_plot_base64 = gm.to_base64(rfc_path)
            xgb_plot_base64 = gm.to_base64(xgb_path)

            handoff={
                'rf_plot': rf_plot_base64,
                'rf_importances' : random_forest_ft_importances[:5],
                'rf_metrics' : random_forest_metrics,
                'xgb_plot': xgb_plot_base64,
                'xgb_importances' : xgb_ft_importances[:5],
                'xgb_metrics' : xgb_metrics}

            # hand-off to html 
            return render(request, 'core/model_results.html', handoff)
        
        print(f"[Error] Models")xw
        return render(request, 'core/home.html')

@login_required
def edit_user_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Optionally create a profile if not found, or handle differently
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'core/home.html')
        
    form = UserProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})



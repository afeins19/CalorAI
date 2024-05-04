"""
URL configuration for mealgen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, reverse_lazy

from core.views import home, signup, login, add_goal, model_results_view, edit_user_profile
from core.forms import LoginForm #, UserAPICredentialsForm

from dailylog.forms import DailyLogform
from dailylog.views import add_daily_log, daily_log_success

urlpatterns = [
    path("admin/", admin.site.urls),

    # custom paths 
    path('', home, name='home' ), # home page path 
    path('login/', LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True, next_page=reverse_lazy('home')), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('signup/', signup, name='signup'),
    path('add_daily_log/', add_daily_log, name='add_daily_log'),
    path('log_success/', daily_log_success, name='daily_log_success'),
    path('model_results/', model_results_view, name='model_results'),
    path('edit_profile/', edit_user_profile, name='edit_profile'),

]

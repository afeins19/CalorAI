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
from django.contrib.auth.views import LoginView
from django.urls import path, include

from core.views import home, signup, login, add_mfp_credentials, add_goal
from core.forms import LoginForm #, UserAPICredentialsForm

from dailylog.forms import DailyLogform
from dailylog.views import add_daily_log, daily_log_success


urlpatterns = [
    path("admin/", admin.site.urls),

    # custom paths 
    path('', home, name='home' ), # home page path 
    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'), # login path 
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),  # includes auth-related URLs
    path('add_mfp_credentials/', add_mfp_credentials, name='add_mfp_credentials'),
    path('add/', add_daily_log, name='add_daily_log'),
    path('success/', daily_log_success, name='daily_log_sucesss'),
]

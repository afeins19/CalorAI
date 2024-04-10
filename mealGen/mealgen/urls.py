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
from core.views import home, signup


from django.contrib.auth.views import LoginView
from core.forms import LoginForm
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),

    # custom paths 
    path('', home, name='home' ), # home page path 
    
    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'), # login path 
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),  # includes auth-related URLs


]

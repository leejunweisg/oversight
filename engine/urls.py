from django.urls import path
from . import views # import views defined in views.py

# blog app urls
urlpatterns = [
    path('', views.dashboard, name='dashboard'), # default home page
    path('dashboard-refresh/', views.dashboard_refresh, name='dashboard-refresh'), # for AJAX refresh
]

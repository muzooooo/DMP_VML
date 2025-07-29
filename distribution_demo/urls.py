# C:\DMP\DMP\distribution_demo\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('distribute/<int:release_id>/', views.distribute_release, name='distribute_release'),
    path('', views.home, name='distribution_home'), # Add a specific home for this app
]
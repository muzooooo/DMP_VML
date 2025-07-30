# C:\DMP\DMP\distribution_demo\urls.py
from django.urls import path
from . import views

app_name = 'distribution_demo' # Keep this line, it's good for namespacing

urlpatterns = [
    path('releases/', views.public_release_list, name='public_release_list'), # <-- ADD THIS LINE
    path('distribute/<int:release_id>/', views.distribute_release, name='distribute_release'),
    path('', views.home, name='distribution_home'),
]
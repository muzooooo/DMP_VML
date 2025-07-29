# C:\DMP\DMP\dmp_project\urls.py
from django.contrib import admin
from django.urls import path, include
from music_publisher.admin import admin_site

# Assuming you have a views.py directly in dmp_project for this home view
from . import views

admin.site.site_header = "Vangarde Music Limited"
admin.site.site_title = "Vangarde Music Limited"
admin.site.index_title = "Welcome back to the Vangarde Music Limited Administrator Terminal"

urlpatterns = [
    # This points the root URL (/) to your dmp_project's home view
    path('', views.home, name='home'),

    # Custom admin site provided by music_publisher
    path('admin/', admin_site.urls),

    # URLs for the music_publisher app (e.g., royalty, CWR exports)
    path('royalty/', include('music_publisher.urls')),

    # URLs for your new distribution_demo app
    # All URLs defined in distribution_demo/urls.py will be prefixed with 'distribution/'
    path('distribution/', include('distribution_demo.urls')),
]
# C:\DMP\DMP\dmp_project\views.py
from django.shortcuts import render # Import the render function

def home(request):
    """
    Renders the public home page for the Vangarde Music Limited site.
    This template extends base.html for consistent site layout.
    """
    return render(request, 'home.html')
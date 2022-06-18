from django.shortcuts import render

# Create your views here.

def plotly1(requests):
    return render(requests, 'plotly_dash/plotly1.html')
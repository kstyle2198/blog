from django.urls import path, include
from . import views
from plotly_dash.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path("plotly1/", views.plotly1)
]
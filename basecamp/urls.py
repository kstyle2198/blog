
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('about_me/', views.about_me),
    path('blog_history/', views.blog_history),
    path('blog_covid/', views.blog_covid),
    path('blog_economy/', views.blog_economy),

]

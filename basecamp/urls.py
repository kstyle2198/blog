
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('about_me/', views.about_me),
    path('blog_history/', views.blog_history),
    path('blog_jarvis/', views.blog_jarvis),
    path('blog_time/', views.blog_time),
    path('blog_repl/', views.blog_repl),

]

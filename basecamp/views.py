from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return redirect('/blog/')

def about_me(request):
    return render(
        request,
        'basecamp/about_me.html'
    )

def blog_history(request):
    return render(
        request,
        'basecamp/blog_history.html'
    )

def blog_covid(request):
    return render(
        request,
        'basecamp/blog_covid.html'
    )

def blog_economy(request):
    return render(
        request,
        'basecamp/blog_economy.html'
    )

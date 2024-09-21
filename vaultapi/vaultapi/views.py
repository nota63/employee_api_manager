from django.shortcuts import render, redirect


#  my views

def home(request):
    return render(request, 'home.html')


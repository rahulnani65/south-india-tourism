from django.shortcuts import render
from .models import State

def home(request):
    states = State.objects.all()
    return render(request, 'core/home.html', {'states': states})
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'Zombies/Home.html',{})
    
    
def login(request):
    return HttpResponse("Login page")

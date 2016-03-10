from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from Zombies.forms import UserForm
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request, 'Zombies/Home.html',{})
    
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/Zombies/')
            else:
                return HttpResponse("Your Zombie account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'Zombies/login.html',{})
    
def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
        
    return render(request,
    'Zombies/registration.html',
    {'user_form': user_form, 'registered':registered})
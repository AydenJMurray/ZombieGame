from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Zombies.forms import UserForm, PlayerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Zombies.models import Player
from django.contrib.auth.models import User

from scripts.main import *

# Create your views here.

def home(request):
	
    kills_list = Player.objects.order_by("-most_kills")[:5]
    days_survived_list = Player.objects.order_by("-most_days_survived")[:5]
    rank_list = [1, 2, 3, 4, 5]
    context_dict={'rank_list':rank_list,'kills_board':kills_list, 'survival_board':days_survived_list}
    return render(request, 'Zombies/Home.html', context_dict)
    
def game_page(request):
    return HttpResponse("Game goes here")

def leaderboard(request):

    return HttpResponse("Leaderboards go here soon")
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
        player_form = PlayerForm(data=request.POST)
        
        if user_form.is_valid() and player_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            player = player_form.save()
            player.user = user
            
            if 'picture' in request.FILES:
                player.profile_picture = request.FILES['profile_picture']
            player.save()
            registered = True
        else:
            print user_form.errors,player_form.errors
    else:
        user_form = UserForm()
        player_form = PlayerForm()
        
    return render(request,
    'Zombies/registration_form.html',
    {'user_form': user_form, 'player_form':player_form ,'registered':registered})


@login_required
def user_logout(request): 
    logout(request)
    return HttpResponseRedirect('/Zombies/')
    
def game_page(request):
    return render(request, 'Zombies/game_page.html',{})

    
def start(request):
    g = Game()
    g.start_new_day()
    game_screen = show_game_screen(g) 
    player_state = g.player_state
    game_state = g.game_state
    turn_options = g.turn_options()
        
    return render(request, 'Zombies/start.html',{'player_state': player_state, 'game_state': game_state,'turn_options': turn_options, 'game_screen':game_screen})
    
def userProfile(request, user_name):
    try:
        user = User.objects.get(username = user_name)
        player = Player.objects.get(user = user)
    except:
        raise Http404('Requested user not found.')
    
    variables = {'user_username':user.username, 'user_email':user.email, 'user_games_played':player.games_played,
                 'user_most_days':player.most_days_survived,'user_most_kills':player.most_kills, 'user_most_people':player.most_people,
                 'user_avg_days':player.avg_days, 'user_avg_kills':player.avg_kills, 'user_avg_people':player.avg_people}
                 

    
    return render(request, 'Zombies/userProfile.html', variables)
    

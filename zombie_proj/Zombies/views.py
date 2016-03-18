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
    context_dict={'kills_board':kills_list, 'survival_board':days_survived_list}
    return render(request, 'Zombies/Home.html', context_dict)
    
def game_page(request):
    return HttpResponse("Game goes here")

def leaderboard(request):
     kills = Player.objects.order_by("-most_kills")[:]
     days = Player.objects.order_by("-most_days_survived")[:]
     people = Player.objects.order_by("-most_people")[:]

     allKills = Player.objects.order_by("-kills_all_time")[:]
     allDays = Player.objects.order_by("-days_all_time")[:]
     allPeople = Player.objects.order_by("-people_all_time")[:]

     context_dict={'kills':kills, 'days':days, 'people':people, 'allKills':allKills,'allDays':allDays ,'allPeople':allPeople }
     return render(request, 'Zombies/leaderboards.html', context_dict)
    
def start(request):
    g = Game()
    g.start_new_day()
    game_screen = show_game_screen(g) 
    player_state = g.player_state
    game_state = g.game_state
    if game_state != "NONE":
        turn_options = g.turn_options()
        
    return render(request, 'Zombies/start.html',{'player_state': player_state, 'game_state': game_state,'turn_options': turn_options})
    
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
    

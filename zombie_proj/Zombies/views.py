from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Zombies.forms import UserForm, PlayerForm
from Zombies.models import *
from django.contrib.auth.models import User
import copy_reg
import pickle
import types
from scripts.main import *
from scripts.game import Game
from scripts.game import PlayerState

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

     
def _pickle_method(g):
    if g.im_self is None:
        return getattr, (g.im_class, g.im_func.func_name)
    else:
        return getattr, (g.im_self, g.im_func.func_name)

def _save(player,g):
    copy_reg.pickle(types.MethodType, _pickle_method)
    player.current_game = pickle.dumps(g)
    player.save()

     
def start(request):
    player = Player.objects.get(user = User.objects.get(username = request.user))
    if player.current_game != None:
        g = pickle.loads(player.current_game)
        if g.is_game_over():
            context_dict = {"game-over": True}
            return render (request, 'Zombies/start.html', context_dict)
        elif g.is_day_over():
            g.end_day()
            g.start_new_day()
    else:
        g = Game()
        g.start_new_day()
    context_dict = dictionary(g)
    _save(player, g)
    return render (request, 'Zombies/start.html', context_dict)
       
    
def turn(request):
    player = Player.objects.get(user)
    g = pickle.loads(player.current_game)
    if turn in ['MOVE','SEARCH']:
        g.take_turn(turn, pos)
    else:
        g.take_turn(turn)
    context_dict = dictionary(g)
    #g.player_state = pickle.loads(pps)
    #g.street = pickle.loads(ps) 
    #g.update_state = pickle.loads(pus)
    _save(player, g)
    return render(request, 'Zombies/start.html',{})
        

    
    

        
def userProfile(request, user_name):
    try:
        user = User.objects.get(username = user_name)
        player = Player.objects.get(user = user)
    except:
        raise Http404('Requested user not found.')
    
    context_dict = {'user_username':user.username, 'user_email':user.email,
                 'user_games_played':player.games_played,
                 'user_most_days':player.most_days_survived,
                 'user_most_kills':player.most_kills,
                 'user_most_people':player.most_people,
                 'user_all_kills':player.kills_all_time, 
                 'user_all_days':player.days_all_time, 
                 'user_all_people':player.people_all_time, 
                 'user_avg_days':player.avg_days,
                 'user_avg_kills':player.avg_kills,
                 'user_avg_people':player.avg_people}
                 

    
    return render(request, 'Zombies/userProfile.html', context_dict)
    

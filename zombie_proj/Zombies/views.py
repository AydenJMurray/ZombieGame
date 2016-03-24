from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Zombies.forms import UserForm, PlayerForm, AddForm
from Zombies.models import *
from django.contrib.auth.models import User
import copy_reg
import pickle
import types
from scripts.main import * 
from scripts.game import Game
from scripts.game import PlayerState
from scripts.house import *
from scripts.streetfactory import *

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
       
    
def turn(request,turn,pos):
    player = Player.objects.get(user = User.objects.get(username = request.user))
    g = pickle.loads(player.current_game)
    turn = str(turn)
    if turn in ['MOVE','SEARCH']:
       pos = int(pos)
       g.take_turn(turn, pos)

    else:
        g.take_turn(turn)
    context_dict = dictionary(g)

    _save(player, g)
    return render(request, 'Zombies/start.html',context_dict)
        

def dictionary(g):
    context_dict = {'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
    'kills':g.player_state.kills,'days':g.player_state.days,  'game_state': g.game_state}
    if g.game_state == 'STREET':
        houseNumbers = []
        houseList = g.street.house_list
        j = 0
        while j <= len(g.street.house_list):
            houseNumbers.append(j)
            j+= 1
        houses = zip(houseNumbers, houseList)
        
        context_dict.update({'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
    'kills':g.player_state.kills,'days':g.player_state.days, 'turn_options':g.turn_options(), 'street': g.street.name, 'game_state': g.game_state,
    'houseList':g.street.house_list,'houses': houses, 'current_house':g.street.get_current_house() })
   
    elif g.game_state == 'HOUSE':
        
        roomNumbers = []
        roomList = g.street.get_current_house().room_list
       
        
        i = 0
            
        while i <= len(g.street.get_current_house().room_list):
           roomNumbers.append(i)
           i += 1
        rooms = zip(roomNumbers , roomList)
        
        context_dict.update({'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
    'kills':g.player_state.kills,'days':g.player_state.days, 'turn_options':g.turn_options(), 'house': True  
    ,'game_state':g.game_state, 'current_house':g.street.get_current_house(),'room_List': g.street.get_current_house().room_list, 'turn_options':g.turn_options(), 'update_state':g.update_state,
     'rooms': rooms,'roomNumbers':roomNumbers, 'update': show_update_template(g),  })
    
    elif g.game_state == 'ZOMBIE':
        context_dict.update({'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
    'kills':g.player_state.kills,'days':g.player_state.days, 'turn_options':g.turn_options(), 'street': g.street.name,  })
    
    return context_dict
    

        
def userProfile(request, user_name):
    try:
        user = User.objects.get(username = user_name)
        player = Player.objects.get(user = user)
    except:
        raise Http404('Requested user not found.')

    curr_user=request.user
    curr_user = User.objects.get(username = curr_user.username)
    curr_player=Player.objects.get(user=curr_user)
    player_friendreq = player.friend_requests
    curr_player_friendreq = curr_player.friend_requests

    form = AddForm(instance=curr_player)

    if (request.method == 'POST') and (curr_player.user.username not in player.friend_requests) and (curr_player.user.username not in player.friends):
        player.friend_requests = curr_user.username
        player.save()
        player_friendreq += ','
        player_friendreq += player.friend_requests
        player.friend_requests = player_friendreq
        player.save()
        if (user_name in curr_player.friend_requests) and (user_name not in curr_player.friends) and (curr_player.user.username in player.friend_requests) and (curr_player.user.username not in player.friends):
            curr_player.friends += ','
            curr_player.friends += user_name
            curr_player_friendreq = curr_player_friendreq.strip(user_name)
            curr_player.friend_requests = curr_player_friendreq
            curr_player.save()
            player.friends += ','
            player.friends += curr_player.user.username
            player_friendreq = player_friendreq.strip(curr_player.user.username)
            player.friend_requests = player_friendreq
            player.save()
    else:
        form = AddForm()
    
    try:
        achievement_list = Achievement.objects.filter(player=player)
        badge_count = achievement_list.count()
    except:
        badge_count = 0
    levels = [0,0,0]
    badge_list = []
    show_badges = []        
    if badge_count > 0:
        for achievement in achievement_list:
            if achievement.badge.level == 'bronze':
                levels[0]+=1
            elif achievement.badge.level == 'silver':
                levels[1]+=1
            else:
                levels[2]+=1
            badge_list.append(achievement.badge)
                 
    	if badge_count == 1:
        	show_badges.append(badge_list[player.badge1_display])
    	elif badge_count ==  2:
        	show_badges.append(badge_list[player.badge1_display])
        	show_badges.append(badge_list[player.badge2_display])
    	elif badge_count == 3:
        	show_badges.append(badge_list[player.badge1_display])
        	show_badges.append(badge_list[player.badge2_display])
        	show_badges.append(badge_list[player.badge3_display])
    	else:
        	show_badges.append(badge_list[player.badge1_display])
        	show_badges.append(badge_list[player.badge2_display])
        	show_badges.append(badge_list[player.badge3_display])
        	show_badges.append(badge_list[player.badge4_display])
        
    friends_list = player.split_friends()
    friends_user_list = []
    for friend in friends_list:
        try:
            friend = User.objects.get(username=friend)
            friends_user_list.append(friend)
        except:
            n = 0
        
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
                    'user_avg_people':player.avg_people,
                    'user_badges':badge_list,
                    'user_badge_levels': levels,
                    'user_badge_count':badge_count,
                    'show_badges' :show_badges,
                    'friends' :friends_user_list}



    
    return render(request, 'Zombies/userProfile.html', context_dict)
    
def new(request):
    player = Player.objects.get(user = User.objects.get(username = request.user))
    player.current_game = None
    player.save()
    return start(request)
    
    
def edit_badges(request):
    user = request.user
    if request.method == 'POST':
        form = PlayerForm(data=request.POST)
        if form.is_valid():
            Player = form.save(commit=True)
            Player.user = request.user
            Player.save()
        else:
            print form.errors
    else:
        form = PlayerForm()
    return render(request, 'Zombies/edit_form.html', {'eform':form, 'user_username':user.username})
    
def add_user(request):
    user=request.user
    user = User.objects.get(username = user.username)
    player=Player.objects.get(user=user)
    player_friends = player.friends
    form = AddForm(instance=player)
    if request.method == 'POST':
        form = AddForm(data=request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            player_friends += ','
            player_friends += player.friends
            player.friends = player_friends

            player.save()
        else:
            print form.errors
        player.friends = player_friends
    else:
        form = AddForm()
    return render(request, 'Zombies/add_user.html', {'aform':form, 'user_username':user.username})
    
def howto(request):
    return render(request, 'Zombies/help.html')



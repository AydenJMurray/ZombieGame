from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Zombies.forms import *
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
    #Checks in user is logged in
    try:
        user = request.user
        player = Player.objects.get(user = user)
        user_login = True
    except:
        user_login = False
        
    #Sets leaderboards
    kills_leaders = Player.objects.order_by("-most_kills")[:5]
    days_leaders = Player.objects.order_by("-most_days_survived")[:5]

    if user_login == True:

        #Get friend requests
        friend_request_list = []
        for friend in player.friend_requests.split(','):
            try:
                friend = User.objects.get(username=friend)
                friend_request_list.append(friend)
            except:
                friend = ''

        #Get friends
        friends_list = []
        friendcount = 0
        for friend in player.split_friends():
            try:
                friend = User.objects.get(username=friend)
                friends_list.append(friend)
                friends = True
                friendcount +=1
            except:
                friend = ''

        n = 0

        #Gets friends leaderboards
        if friends == True:
            friends_leaders = []
            
            while n < 4 and n < friendcount :
                max_player = Player.objects.order_by("most_kills")[:1]
                for player in max_player:
                    pr = player
                max_player = pr
                for friend in friends_list:
                    player = Player.objects.get(user = friend)
                    if player.most_kills >= max_player.most_kills and player not in friends_leaders:
                        max_player = player
                friends_leaders.append(max_player)
                n += 1
        else:
            friends_leaders = []

        #If user searches and is valid request user profile
        form = SearchForm()
        if request.method == 'POST':
            form = SearchForm(data=request.POST)
            if form.is_valid():
                search = form.data['search']
                return userProfile(request, search)
            else:
                print form.errors
        else:
            form = SearchForm()

        #Set context_dict
        context_dict={'kills_board':kills_leaders, 'survival_board':days_leaders,
                  'friends_board':friends_leaders,'friend_requests':friend_request_list,
                  'friends':friends_list, 'aform':form,
                  'user_login':user_login}
    else:
        
        context_dict={'kills_board':kills_leaders, 'survival_board':days_leaders,
                    'user_login':user_login}
    
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
            context_dict = {"game_over": True}
            return render (request, 'Zombies/start.html', context_dict)
        elif g.is_day_over():
            g.end_day()
            context_dict = {'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
            'kills':g.player_state.kills,'days':g.player_state.days,  'game_state': g.game_state,'time_left':g.time_left }
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
    if g.is_game_over():
        context_dict = {'game_over':True}
        return render (request, 'Zombies/start.html', context_dict)
    elif g.is_day_over():
        g.end_day()
        context_dict = {'day_end': g.player_state.days,'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
            'kills':g.player_state.kills,'days':g.player_state.days,  'game_state': g.game_state,'time_left':g.time_left }
        g.start_new_day()
    _save(player, g)
    return render(request, 'Zombies/start.html',context_dict)
        

def dictionary(g):
    context_dict = {'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
    'kills':g.player_state.kills,'days':g.player_state.days,  'game_state': g.game_state,'time_left':g.time_left}
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
    'houseList':g.street.house_list,'houses': houses, 'current_house':g.street.get_current_house(), 'time_left':g.time_left, 'house_numbers': houseNumbers})
   
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
     'rooms': rooms,'roomNumbers':roomNumbers, 'update': show_update_template(g), 'time_left':g.time_left, 'Visited': g.street.get_current_house().get_current_room().visited })
    
    elif g.game_state == 'ZOMBIE':
        context_dict.update({'party':g.player_state.party, 'ammo':g.player_state.ammo, 'food':g.player_state.food,
    'kills':g.player_state.kills,'days':g.player_state.days, 'turn_options':g.turn_options(), 'time_left':g.time_left,
    'zombie': True, 'zombies': g.street.get_current_house().get_current_room().zombies })
    
    return context_dict
    

        
def userProfile(request, user_name):

    ##Get page user/player and current user/player and friend requests
    try:
        page_user = User.objects.get(username = user_name)
        page_player = Player.objects.get(user = page_user)
    except:
        raise Http404('Requested user not found.')

    curr_user=request.user
    curr_player=Player.objects.get(user=curr_user)
    page_player_friendreq = page_player.friend_requests
    curr_player_friendreq = curr_player.friend_requests


    form = AddForm(instance=curr_player)
    #If clicked add friend, and user is not on profile users friend requests, and user is not in profile users friends
    if (request.method == 'POST') and (curr_player.user.username not in page_player.friend_requests) and (curr_player.user.username not in page_player.friends):
        #Add to friend requests
        page_player.friend_requests = curr_user.username
        page_player.save()
        page_player_friendreq += ','
        page_player_friendreq += player.friend_requests
        page_player.friend_requests = player_friendreq
        page_player.save()
        #If profile user is in current players friend requests but not friends and vice versa
        if (user_name in curr_player.friend_requests) and (user_name not in curr_player.friends) and (curr_player.user.username in player.friend_requests) and (curr_player.user.username not in player.friends):
            #Add friends to friends list for both players and delete from friends list
            curr_player.friends += ','
            curr_player.friends += user_name
            curr_player_friendreq = curr_player_friendreq.strip(user_name)
            curr_player.friend_requests = curr_player_friendreq
            curr_player.save()
            page_player.friends += ','
            page_player.friends += curr_player.user.username
            page_player_friendreq = page_player_friendreq.strip(curr_player.user.username)
            page_player.friend_requests = page_player_friendreq
            page_player.save()
    else:
        form = AddForm()

    #Try get the achievement list
    try:
        achievement_list = Achievement.objects.filter(player=page_player)
        badge_count = achievement_list.count()
    except:
        badge_count = 0
    
    levels = [0,0,0]
    badge_list = []
    show_badge_number = [page_player.badge1_display, page_player.badge2_display, page_player.badge3_display, page_player.badge4_display]
    show_badges = []
    #If page user has badges
    if badge_count > 0:
        for achievement in achievement_list:
            #For all achievements, check what level they are and record number of broze silver and gold
            if achievement.badge.level == 'bronze':
                levels[0]+=1
            elif achievement.badge.level == 'silver':
                levels[1]+=1
            else:
                levels[2]+=1
            #Add badge to badgelist
            badge_list.append(achievement.badge)

        #Add badges to badge showcase
        n = 0
        while n < 4 and n < badge_count:
            show_badges.append(badge_list[show_badge_number[n]])
            n+=1
    #Set friendList
    friends_list = page_player.split_friends()
    friends_user_list = []
    for friend in friends_list:
        try:
            friend = User.objects.get(username=friend)
            friends_user_list.append(friend)
        except:
            n = 0

        
    context_dict = {'user_username':page_user.username, 'user_email':page_user.email,
                    'user_games_played':page_player.games_played,
                    'user_most_days':page_player.most_days_survived,
                    'user_most_kills':page_player.most_kills,
                    'user_most_people':page_player.most_people,
                    'user_all_kills':page_player.kills_all_time, 
                    'user_all_days':page_player.days_all_time, 
                    'user_all_people':page_player.people_all_time, 
                    'user_avg_days':page_player.avg_days,
                    'user_avg_kills':page_player.avg_kills,
                    'user_avg_people':page_player.avg_people,
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



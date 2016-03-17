__author__ = 'leif'
import math
import random
from streetfactory import StreetFactory
from copy import deepcopy

MAX_MOVE_TIME = 10
MAX_SEARCH_TIME = 5
WAIT_TIME = 20
FIGHT_TIME = 5
RUN_TIME = 2
ENTER_TIME = 1
EXIT_TIME = 1
NONE_TIME = 0
LENGTH_OF_DAY = 100

class PlayerState(object):

    def __init__(self):
        self.party = 1
        self.ammo = 2
        self.food = 3
        self.kills = 0
        self.days = 0

    @property
    def move_time(self):
        """
        As party size gets bigger the time to move is reduced
        :return: an integer denoting the amount of time
        """
        return MAX_MOVE_TIME - (math.floor(min(math.log(self.party),MAX_MOVE_TIME) / 2))


    @property
    def search_time(self):
        """
        As party size gets bigger the time to search is reduced
        :return:
        """
        return MAX_SEARCH_TIME  - (math.floor(min(self.party, MAX_SEARCH_TIME)/2))


    def __str__(self):
        return 'People: {party} Food: {food} Ammo: {ammo} Kills: {kills} Days: {days}'.format(**self.__dict__)


ACTIONS = {
    'STREET': ['MOVE','ENTER','WAIT'],
    'HOUSE': ['SEARCH','EXIT','WAIT'],
    'ZOMBIE': ['FIGHT','RUN','WAIT'],
    }

class Game(object):

    def __init__(self):
        self.update_state = PlayerState()
        self.update_state.food = 0
        self.update_state.ammo = 0
        self.update_state.kills = 0
        self.update_state.party = 0

        self.player_state = PlayerState()

        self._time_left = LENGTH_OF_DAY
        self.street_factory = StreetFactory()
        self.game_state = None

    @property
    def time_left(self):
        return self._time_left


    def update_time_left(self, time_spent):
        self._time_left -= time_spent

    def turn_options(self):
        return ACTIONS[self.game_state]


    def take_turn(self, action, value=None):

        def diff_state(state_a, state_b):
            state = PlayerState()
            state.party = state_a.party - state_b.party
            state.food = state_a.food - state_b.food
            state.ammo = state_a.ammo - state_b.ammo
            state.kills = state_a.kills - state_b.kills
            state.days = state_a.days - state_b.days
            return state

        turn_actions ={
            'MOVE': self.__action_move,
            'ENTER': self.__action_enter,
            'WAIT': self.__action_wait,
            'SEARCH': self.__action_search,
            'EXIT': self.__action_exit,
            'FIGHT': self.__action_fight,
            'RUN': self.__action_run,
        }

        # save current player state
        player_last_state = deepcopy(self.player_state)

        if action in self.turn_options():
            turn_actions[action](value)
        else:
            pass

        state_change = diff_state(self.player_state,player_last_state)
        self.update_state = state_change




    def start_new_day(self):
        self.player_state.days += 1
        self._time_left = LENGTH_OF_DAY
        self.street = self.street_factory.make_street(self.player_state)
        self.game_state = 'STREET'



    def end_day(self):
        # update the amount of food left.
        food = self.player_state.food
        people = self.player_state.party
        leavers = 0

        self.update_state.days = 1
        # if there is not enough food some people leave.
        if people > food:
            leavers = random.randint(1, people - food)
            self.player_state.party = people - leavers
            self.player_state.food = 0
        else:
            self.player_state.food = food - people



    def is_day_over(self):

        if self.time_left <= 0:
            return True
        else:
            return False

    def is_game_over(self):
        """
        :return: True if the game is over, i.e. if the party_size is zero
        """
        if self.player_state.party <= 0:
            return True
        else:
            return False


    def __action_move(self, value=None):

        # Update where the Player is. i.e. which house are they infront of
        moved = False
        if value is None:
            moved = self.street.move_to_next_house()
        else:
            moved = self.street.move_to_house(value)
        if moved:

            self.update_time_left(self.player_state.move_time)
            self.game_state = 'STREET'


    def __action_enter(self, value=None):

        # player enters the current house.

        self.update_time_left(ENTER_TIME)
        self.game_state = 'HOUSE'


    def __action_wait(self, value=None):

        self.update_time_left(WAIT_TIME)


    def __action_search(self, value=None):

        # need to select which room to search
        selected = False
        if value is None:
            selected = self.street.get_current_house().move_to_room(0)
        else:
            selected = self.street.get_current_house().move_to_room(value)

        if selected:
            current_room = self.street.get_current_house().get_current_room()
            #print current_room
            if current_room.zombies > 0:
                self.game_state = 'ZOMBIE'
            else:
                self.__player_clears_room(current_room)
                self.game_state = 'HOUSE'


    def __action_exit(self, value=None):

        self.update_time_left(EXIT_TIME)
        self.game_state = 'STREET'
        self.current_room = None


    def __action_fight(self, value=None):

        self.update_time_left(FIGHT_TIME)

        current_room = self.street.get_current_house().get_current_room()
        zombies = current_room.zombies
        ammo = current_room.ammo
        self.__player_attacks_with_ammo(current_room)

        p_loss = 0.15+(zombies*0.02)-(ammo*0.01)
        self.__player_attacked_by_zombie(p_loss)

        if current_room.zombies > 0:
            p_win= 0.3 + max(0.01 * self.player_state.party, 0.15)
            self.__player_attacks_without_ammo(current_room, p_win)

        if current_room.zombies <= 0:
            self.__player_clears_room(current_room)
            self.game_state = 'HOUSE'

        else:
            self.game_state = 'ZOMBIE'


    def __action_run(self, value=None):

        self.update_time_left(RUN_TIME)
        self.__player_attacked_by_zombie(0.4)
        self.game_state = 'STREET'


    def __action_none(self, value=None):

        self.update_time_left(NONE_TIME)



    def __player_clears_room(self, current_room):

        self.player_state.food += current_room.food
        self.player_state.party += current_room.people
        self.player_state.ammo += current_room.ammo
        current_room.cleared()
        self.update_time_left(self.player_state.search_time)


    def __player_attacked_by_zombie(self, p_loss = 0.2):
        p = random.uniform(0,1)
        if p < p_loss:
            self.player_state.party -= random.randint(1,max(3,self.player_state.party))


    def __player_attacks_without_ammo(self, current_room, p_win=0.3):

        zombies = current_room.zombies
        p = random.uniform(0,1)
        if p < p_win:
            kills = current_room.zombies
            current_room.zombies = zombies - kills
            self.player_state.kills += kills

    def __player_attacks_with_ammo(self, current_room, p_win=1.0):

        zombies = current_room.zombies
        ammo = self.player_state.ammo
        kills = min(ammo, zombies)
        current_room.zombies = zombies - kills
        self.player_state.ammo -= kills
        self.player_state.kills += kills

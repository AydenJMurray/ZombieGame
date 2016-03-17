__author__ = 'leif'

import os
from game import Game
from streetfactory import StreetFactory
from game import PlayerState



def main():

    # this is the basic game process
    # while the day or game is not over,
    # display the current state of the game,
    # then check what the player wants to do

    g = Game()
    while not g.is_game_over():
        #kick off the day
        g.start_new_day()
        while not g.is_day_over() and not g.is_game_over():
            os.system("clear")
            show_game_screen(g)

            turn_options(g)

        # end the day
        g.end_day()


    print "Aaarrrgh: You are dead! Game Over!"




def show_game_screen(g):
    print ""
    print "------------------------------------------"
    print "ZZZZZ   OOO    MM    MM  BBBB   III  EEEEE"
    print "   Z   OO OO   MMM  MMM  B   B   I   E"
    print "  Z   OO   OO  MM MM MM  BBBB    I   EEE"
    print " Z     OO OO   MM    MM  B   B   I   E"
    print "ZZZZZ   OOO    MM    MM  BBBBB  III  EEEEE"
    print "------------------------------------------"
    print ""
    print "Player Status"
    print "------------------------------------------"
    print g.player_state
    print ""
    print "Day: {0}, Time left in day: {1}".format(g.player_state.days, g.time_left)
    print "------------------------------------------"

    show_update_template(g)

    print "------------------------------------------"
    if g.game_state == 'STREET':
        show_street_template(g)
    if g.game_state == 'HOUSE':
        show_house_template(g)
    if g.game_state == 'ZOMBIE':
        show_zombie_template(g)

    print "------------------------------------------"


def turn_options(g):
    print ""
    print "Available options:"
    print g.turn_options()
    print "------------------------"
    turn = raw_input('What do you want to do (enter full word i.e. MOVE, SEARCH, etc): ')

    if turn in ['MOVE','SEARCH']:
        pos = int(raw_input('where (enter number of house/room): '))
        g.take_turn(turn, pos)
    else:
        g.take_turn(turn)


def show_street_template(g):
    print "You are in a Street!"
    print g.street
    i = 0
    for house in g.street.house_list:

        print "House: ", i, house

        i += 1
    print ""
    print "------------------------------------------"
    print "You are out the front of:"
    print g.street.get_current_house()

def show_house_template(g):
    print "You are in a house!"
    print g.street.get_current_house()
    print g.street.get_current_house().get_current_room()

def show_zombie_template(g):
    current_room = g.street.get_current_house().get_current_room()
    print "zaarrrr rrrgh: {0} Zombies!!!!".format(current_room.zombies)


def show_update_template(g):

    if g.update_state.party<0:
        print "You lost: {0} people".format(abs(g.update_state.party))

    if g.update_state.party>0:
        print "{0} more people have joined your party".format(g.update_state.party)

    if g.update_state.ammo > 0:
        print "You found: {0} units of ammo".format(g.update_state.ammo)

    if g.update_state.ammo < 0:
        print "You used: {0} units of ammo".format(abs(g.update_state.ammo))

    if g.update_state.food > 0:
        print "You found: {0} units of food".format(g.update_state.food)

    if g.update_state.food < 0:
        print "You used: {0} units of food".format(abs(g.update_state.food))

    if g.update_state.kills > 0:
        print "You killed: {0} zombies".format(g.update_state.kills)

    if g.update_state.days > 0:
        print "New Day: You survived another day!"

if __name__ ==  "__main__":
    main()
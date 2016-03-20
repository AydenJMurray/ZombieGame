import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zombie_proj.settings')

import django
django.setup()

from django.contrib.auth.models import User
from Zombies.models import Player


def populate():

    add_player(user=add_user("Jim"),
               games=3,
               kills=12,
               days_survived=31,
               people=5)

    add_player(user=add_user("Jean"),
               games=6,
               kills=32,
               days_survived=10,
               people=4)

    add_player(user=add_user("Joe"),
               games=1,
               kills=0,
               days_survived=2,
               people=1)

    add_player(user=add_user("Jack"),
               games=2,
               kills=3,
               days_survived=1,
               people=1)

    add_player(user=add_user("Jill"),
               games=6,
               kills=23,
               days_survived=8,
               people=2)

    add_player(user=add_user("Jessica"),
               games=8,
               kills=9,
               days_survived=12,
               people=4)

    add_player(user=add_user("Jacob"),
               games=9,
               kills=21,
               days_survived=21,
               people=4)

    add_player(user=add_user("Jackie"),
               games=12,
               kills=7,
               days_survived=7,
               people=7)

    add_player(user=add_user("James"),
               games=3,
               kills=6,
               days_survived=6,
               people=6)

    add_player(user=add_user("Jenny"),
               games=1,
               kills=2,
               days_survived=13,
               people=7)

    add_player(user=add_user("ToniG"),
               games=42,
               kills=42,
               days_survived=42,
               people=42)

    # Print out what we have added to the user.
    #for p in Player.objects.all():
           # print "- {0} - {1}".format(str(p))

def add_user(username):
    u = User.objects.get_or_create(username=username)[0]
    u.save()
    return u

def add_player(user, games, kills, days_survived, people):
    p = Player.objects.get_or_create(user=user, games_played=games, most_kills=kills, most_days_survived=days_survived, most_people=people)[0]
    p.save()
    return p



# Start execution here!
if __name__ == '__main__':
    print "Starting leaderboard population script..."
    populate()

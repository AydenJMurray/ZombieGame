
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    games_played = models.IntegerField(default=0)
    most_days_survived = models.IntegerField(default = 0)
    most_kills = models.IntegerField(default = 0)
    most_people = models.IntegerField(default = 0)
    kills_all_time = models.IntegerField(default=0)
    days_all_time = models.IntegerField(default=0)
    people_all_time= models.IntegerField(default=0)
    current_game = models.CharField(max_length = 1024,blank=True, null=True)
    badge1_display = models.IntegerField(max_length = 2, null=True, default = 0)
    badge2_display = models.IntegerField(max_length = 2, null=True, default = 1)
    badge3_display = models.IntegerField(max_length = 2, null=True, default = 2)
    badge4_display = models.IntegerField(max_length = 2, null=True, default = 3)
    friends = models.CharField(max_length=1000, default="bob,Jill,")
    def split_friends(self):
        return self.friends.split(',')



    def getAvgDays(self):
        if self.games_played > 0: 
            return self.days_all_time/self.games_played
        return 0

    def getAvgKills(self):
        if self.games_played > 0: 
            return self.kills_all_time/self.games_played
        return 0

    def getAvgPeople(self):
        if self.games_played > 0: 
            return self.people_all_time/self.games_played
        return 0

    avg_days = property(getAvgDays) 
    avg_kills = property(getAvgKills) 
    avg_people = property(getAvgPeople) 

    def __unicode__(self):
        return self.user.username

		
class Badge(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=64)
    criteria = models.IntegerField()
    badge_type = models.CharField(max_length = 10)
    level = models.CharField(max_length = 10)
    
    class Meta:
        unique_together = (('name','level'))


class Achievement(models.Model):
    player = models.ForeignKey('Player')
    badge = models.ForeignKey('Badge')
    date_awarded = models.TimeField(auto_now_add=True)
    class Meta:
        unique_together = (('player','badge'))

# class Game(models.Model):
    # #user = models.ForeignKey('Player')
    # game_state = models.CharField(max_length=128)
    # player_state = models.CharField(max_length=128)#player_state
    # street = models.CharField(max_length=128)#street
    # update_state = models.CharField(max_length=128)#update_state
	


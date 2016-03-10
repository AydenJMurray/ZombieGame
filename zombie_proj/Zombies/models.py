

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.username


class Player(models.Model):
    user = models.OneToOneField('User', unique = True)

#<<<<<<< HEAD
    profile_picture = models.ImageField(height_field=None, width_field=None ,max_length=100)
#=======
    profile_picture = models.ImageField(max_length=100)

    games_played = models.IntegerField()
    most_days_survived = models.IntegerField()
    most_kills = models.IntegerField()
    most_people = models.IntegerField()
    avg_days = models.DecimalField(max_digits = 5, decimal_places = 1)
    avg_kills = models.DecimalField(max_digits = 5, decimal_places = 1)
    avg_people = models.DecimalField(max_digits = 5, decimal_places = 1)
    current_game = models.FileField(max_length = 100)
    def __unicode__(self):
        return self.user.username

class Badge(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=64)
    criteria = models.IntegerField()
    badge_type = models.CharField(max_length = 10)
    level = models.CharField(max_length = 10)

#<<<<<<< HEAD
    icon = models.ImageField(height_field=None, width_field=None ,max_length=100)
#=======
    icon = models.ImageField(max_length=100)

    
    class Meta:
        unique_together = (('name','level'))





class Achievement(models.Model):
    player = models.ForeignKey('Player')
    badge = models.ForeignKey('Badge')
    date_awarded = models.TimeField(auto_now_add=True)
    class Meta:
        unique_together = (('player','badge'))


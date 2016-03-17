
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
#class User(models.Model):
    #user = models.OneToOneField(User)
    
    #def __unicode__(self):
        #return self.user.username


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    games_played = models.IntegerField(blank=True, null=True)
    most_days_survived = models.IntegerField(blank=True, null=True)
    most_kills = models.IntegerField(blank=True, null=True)
    most_people = models.IntegerField(blank=True, null=True)
    avg_days = models.DecimalField(max_digits = 5, decimal_places = 1,blank=True, null=True)
    avg_kills = models.DecimalField(max_digits = 5, decimal_places = 1,blank=True, null=True)
    avg_people = models.DecimalField(max_digits = 5, decimal_places = 1,blank=True, null=True)
    current_game = models.FileField(max_length = 100,blank=True, null=True)
    def __unicode__(self):
        return self.user.username

		
class Badge(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=64)
    criteria = models.IntegerField()
    badge_type = models.CharField(max_length = 10)
    level = models.CharField(max_length = 10)
    icon = models.ImageField(height_field=None, width_field=None ,max_length=100)
    icon = models.ImageField(max_length=100)
 
    class Meta:
        unique_together = (('name','level'))


class Achievement(models.Model):
    player = models.ForeignKey('Player')
    badge = models.ForeignKey('Badge')
    date_awarded = models.TimeField(auto_now_add=True)
    class Meta:
        unique_together = (('player','badge'))

	


from django.db import models

# Create your models here.
class User(models.Model):
    username = model.CharField(max_length=128, unique=True)
    password = model.CharField(max_length=64)
    email = model.EmailField(max_length=75)
    def __unicode__(self):
        return self.username


class Player(models.Model):
    user = model.OneToOneField('User', unique = True)
    profile_picture = model.ImageField(height_field=none, width_field=none ,max_length=100)
    games_played = model.IntegerField()
    most_days_survived = model.IntegerField()
    most_kills = model.IntegerField()
    most_people = model.IntegerField()
    avg_days = model.DecimalField(max_digits = 5, decimal_places = 1)
    avg_kills = model.DecimalField(max_digits = 5, decimal_places = 1)
    avg_people = model.DecimalField(max_digits = 5, decimal_places = 1)
    current_game = model.FileField(max_length = 100)
    def __unicode__(self):
        return self.user.username




class Acheivement(models.Model):
    player = model.ForeignKey('Player')
    badge = model.ForeignKey('Badge')
    date_awarded = model.TimeField(auto_now_add=True)
    class Meta:
        unique_together = (('player','badge'))


class Badge(models.Model):
    name = model.CharField(max_length=128)
    description = model.CharField(max_length=64)
    criteria = model.IntegerField()
    badge_type = model.CharField(max_length = 10)
    level = model.CharField(max_length = 10)
    icon = model.ImageField(height_field=none, width_field=none ,max_length=100)
    
    class Meta:
        unique_together = (('name','level'))

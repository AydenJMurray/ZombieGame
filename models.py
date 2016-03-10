from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=75)
    def __unicode__(self):
        return self.username


class Player(models.Model):
    user = models.OneToOneField('User', unique = True)
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
    icon = models.ImageField(max_length=100)
    
    class Meta:
        unique_together = (('name','level'))


class Achievement(models.Model):
    player = models.ForeignKey('Player')
    badge = models.ForeignKey('Badge')
    date_awarded = models.TimeField(auto_now_add=True)
    class Meta:
        unique_together = (('player','badge'))



from django.contrib import admin
from Zombies.models import User, Player, Badge, Achievement
# Register your models here.

admin.site.register(User)
admin.site.register(Player)
admin.site.register(Badge)
admin.site.register(Achievement)

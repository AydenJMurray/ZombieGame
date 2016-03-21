# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0015_remove_game_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='pps',
            new_name='player_state',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='ps',
            new_name='street',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='pus',
            new_name='update_state',
        ),
    ]

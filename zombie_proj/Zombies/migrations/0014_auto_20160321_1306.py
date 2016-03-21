# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0013_game'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='player_state',
            new_name='pps',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='street_state',
            new_name='ps',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='update_state',
            new_name='pus',
        ),
    ]

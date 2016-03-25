# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0024_auto_20160325_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='games_completed',
            new_name='games_played',
        ),
    ]

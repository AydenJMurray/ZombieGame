# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0023_auto_20160324_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='games_played',
            new_name='games_completed',
        ),
    ]

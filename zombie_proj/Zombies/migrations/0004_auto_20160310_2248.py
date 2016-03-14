# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0003_auto_20160310_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='games_played',
            field=models.IntegerField(blank=True),
        ),
    ]

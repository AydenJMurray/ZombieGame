# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0005_auto_20160310_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='games_played',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

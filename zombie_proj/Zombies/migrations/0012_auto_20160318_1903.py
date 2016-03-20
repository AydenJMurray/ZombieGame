# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0011_auto_20160315_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='avg_days',
        ),
        migrations.RemoveField(
            model_name='player',
            name='avg_kills',
        ),
        migrations.RemoveField(
            model_name='player',
            name='avg_people',
        ),
        migrations.AddField(
            model_name='player',
            name='days_all_time',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='kills_all_time',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='people_all_time',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='games_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='most_days_survived',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='most_kills',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='most_people',
            field=models.IntegerField(default=0),
        ),
    ]

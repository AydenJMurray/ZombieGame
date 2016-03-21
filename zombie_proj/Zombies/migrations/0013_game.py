# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0012_auto_20160318_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_state', models.CharField(max_length=128)),
                ('player_state', models.CharField(max_length=128)),
                ('street_state', models.CharField(max_length=128)),
                ('update_state', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to='Zombies.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

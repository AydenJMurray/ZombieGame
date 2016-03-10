# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_awarded', models.TimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=64)),
                ('criteria', models.IntegerField()),
                ('badge_type', models.CharField(max_length=10)),
                ('level', models.CharField(max_length=10)),
                ('icon', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_picture', models.ImageField(upload_to=b'')),
                ('games_played', models.IntegerField()),
                ('most_days_survived', models.IntegerField()),
                ('most_kills', models.IntegerField()),
                ('most_people', models.IntegerField()),
                ('avg_days', models.DecimalField(max_digits=5, decimal_places=1)),
                ('avg_kills', models.DecimalField(max_digits=5, decimal_places=1)),
                ('avg_people', models.DecimalField(max_digits=5, decimal_places=1)),
                ('current_game', models.FileField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=128)),
                ('password', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to='Zombies.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='badge',
            unique_together=set([('name', 'level')]),
        ),
        migrations.AddField(
            model_name='achievement',
            name='badge',
            field=models.ForeignKey(to='Zombies.Badge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='achievement',
            name='player',
            field=models.ForeignKey(to='Zombies.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='achievement',
            unique_together=set([('player', 'badge')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0018_auto_20160321_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='player',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='player',
            name='badge1_display',
            field=models.IntegerField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='badge2_display',
            field=models.IntegerField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='badge3_display',
            field=models.IntegerField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='badge4_display',
            field=models.IntegerField(max_length=2, null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0020_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='friends',
            field=models.CharField(default=b'bob,Jill,', max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='badge1_display',
            field=models.IntegerField(default=0, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='badge2_display',
            field=models.IntegerField(default=1, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='badge3_display',
            field=models.IntegerField(default=2, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='badge4_display',
            field=models.IntegerField(default=3, max_length=2, null=True),
        ),
    ]

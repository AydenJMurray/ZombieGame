# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0017_auto_20160321_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='current_game',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0021_auto_20160322_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='friends',
            field=models.CharField(default=b'bob,', max_length=1000),
        ),
    ]

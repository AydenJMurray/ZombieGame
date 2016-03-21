# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0014_auto_20160321_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='user',
        ),
    ]

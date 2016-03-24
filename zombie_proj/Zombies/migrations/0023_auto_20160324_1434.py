# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0022_auto_20160323_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='friend_requests',
            field=models.CharField(default=b'none', max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='friends',
            field=models.CharField(default=b'none', max_length=1000),
        ),
    ]

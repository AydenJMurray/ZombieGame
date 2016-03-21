# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0016_auto_20160321_1559'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.AlterField(
            model_name='player',
            name='current_game',
            field=models.FileField(max_length=1024, null=True, upload_to=b'', blank=True),
        ),
    ]

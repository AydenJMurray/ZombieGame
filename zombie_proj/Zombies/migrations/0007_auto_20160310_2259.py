# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zombies', '0006_auto_20160310_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='avg_days',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='avg_kills',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='avg_people',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='current_game',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='most_days_survived',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='most_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='most_people',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_databaseentry_youtube_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='databaseentry',
            name='initial_data_hash',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AddField(
            model_name='databaseentry',
            name='validated',
            field=models.BooleanField(default=True),
        ),
    ]

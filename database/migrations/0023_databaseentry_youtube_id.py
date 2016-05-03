# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0022_auto_20160308_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='databaseentry',
            name='youtube_id',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]

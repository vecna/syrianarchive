# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_auto_20160308_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationplace',
            name='name',
            field=models.CharField(unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='locationplace',
            name='name_ar',
            field=models.CharField(max_length=250, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='locationplace',
            name='name_en',
            field=models.CharField(max_length=250, unique=True, null=True),
        ),
    ]

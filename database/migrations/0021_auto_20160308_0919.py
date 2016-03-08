# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_auto_20150807_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='description_ar',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='description_en',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='name_ar',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='name_en',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='reference_code',
            field=models.CharField(default=b'2016-03-08 09:19:58.616658+00:00', unique=True, max_length=250),
            preserve_default=False,
        ),
    ]

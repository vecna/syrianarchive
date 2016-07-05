# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0024_auto_20160705_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databaseentry',
            name='initial_data_hash',
            field=models.CharField(default=b'', max_length=500, editable=False),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='name',
            field=models.CharField(default=b'', max_length=250),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='name_ar',
            field=models.CharField(default=b'', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='name_en',
            field=models.CharField(default=b'', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='databaseentry',
            name='reference_code',
            field=models.CharField(default=b'0eb411a9-6358-4ef1-a7b7-0764e1cfb26c', unique=True, max_length=250),
        ),
    ]

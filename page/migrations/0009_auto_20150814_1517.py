# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0008_auto_20150523_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='linked_pages',
            field=models.ManyToManyField(related_name='linked_pages_rel_+', to='page.Page', blank=True),
        ),
    ]

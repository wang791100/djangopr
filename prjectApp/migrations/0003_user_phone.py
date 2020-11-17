# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prjectApp', '0002_auto_20201102_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=12345678910L, max_length=15, verbose_name='\u7535\u8bdd\u53f7\u7801'),
        ),
    ]

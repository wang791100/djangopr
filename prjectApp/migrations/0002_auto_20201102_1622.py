# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prjectApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='count',
            field=models.IntegerField(default=10, verbose_name='\u62bd\u5956\u6b21\u6570'),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.IntegerField(default=1, verbose_name='\u5145\u503c\u6b21\u6570'),
        ),
    ]

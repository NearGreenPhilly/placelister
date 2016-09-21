# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listr', '0003_auto_20160908_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='neighborhood',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='place',
            name='zip_code',
            field=models.CharField(max_length=5, null=True),
            preserve_default=True,
        ),
    ]

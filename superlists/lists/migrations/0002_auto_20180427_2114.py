# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.AddField(
            model_name='item',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

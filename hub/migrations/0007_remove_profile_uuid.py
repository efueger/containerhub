# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 13:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0006_auto_20161228_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='uuid',
        ),
    ]

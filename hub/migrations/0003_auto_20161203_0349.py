# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 02:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0002_auto_20161203_0334'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.GenericIPAddressField()),
                ('subnet', models.PositiveSmallIntegerField()),
                ('gateway', models.GenericIPAddressField()),
            ],
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.Network'),
        ),
    ]

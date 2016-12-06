# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 02:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSHKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('public_key', models.CharField(max_length=4096)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='container',
            options={'ordering': ('owner', 'name')},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('user',)},
        ),
        migrations.AddField(
            model_name='container',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
